#!/usr/bin/env python3
import base64
import email
from datetime import datetime, timedelta
from gmail_auth import get_gmail_service

def decode_message(msg):
    payload = msg.get('payload', {})
    
    subject = ''
    sender = ''
    body = ''
    
    # Extraire les en-têtes
    headers = payload.get('headers', [])
    
    for h in headers:
        name = h.get('name', '')
        value = h.get('value', '')
        
        if name == 'Subject':
            subject = value
        elif name == 'From':
            sender = value
    
    def get_body_from_payload(p):
        # Nettoyage HTML basique
        import re
        
        if 'parts' in p:
            # Chercher d'abord du texte plain
            for part in p['parts']:
                if part.get('mimeType') == 'text/plain':
                    if 'body' in part and 'data' in part['body']:
                        return base64.urlsafe_b64decode(part['body']['data'].encode('ASCII')).decode('utf-8', errors='ignore')
            
            # Sinon chercher du HTML et le nettoyer
            for part in p['parts']:
                if part.get('mimeType') == 'text/html':
                    if 'body' in part and 'data' in part['body']:
                        html = base64.urlsafe_b64decode(part['body']['data'].encode('ASCII')).decode('utf-8', errors='ignore')
                        # Nettoyage HTML simple
                        clean = re.sub(r'<[^>]+>', '\n', html)
                        clean = re.sub(r'\n+', '\n', clean)
                        return clean.strip()
            
            # Récursion pour les parties imbriquées
            for part in p['parts']:
                body = get_body_from_payload(part)
                if body:
                    return body
        else:
            if 'body' in p and 'data' in p['body']:
                data = base64.urlsafe_b64decode(p['body']['data'].encode('ASCII')).decode('utf-8', errors='ignore')
                # Si c'est du HTML, le nettoyer
                if '<html' in data.lower() or '<div' in data.lower():
                    clean = re.sub(r'<[^>]+>', '\n', data)
                    clean = re.sub(r'\n+', '\n', clean)
                    return clean.strip()
                return data
        return ''
    
    body = get_body_from_payload(payload)
    
    return {'subject': subject, 'sender': sender, 'body': body}

def get_recent_emails(service, days=0, max_emails=None):
    # Récupère TOUS les emails de l'inbox si days=0 et max_emails=None
    if days > 0:
        yesterday = datetime.now() - timedelta(days=days)
        query = f'in:inbox after:{yesterday.strftime("%Y/%m/%d")}'
    else:
        query = 'in:inbox'
    
    # Récupération avec pagination pour avoir tous les emails
    messages = []
    next_page_token = None
    
    while True:
        results = service.users().messages().list(
            userId='me', 
            q=query, 
            pageToken=next_page_token
        ).execute()
        
        batch = results.get('messages', [])
        messages.extend(batch)
        
        next_page_token = results.get('nextPageToken')
        
        # Si pas de limite définie, on continue jusqu'à la fin
        if max_emails and len(messages) >= max_emails:
            break
        
        # Si plus de pages, on arrête
        if not next_page_token:
            break
    
    # Trier par date interne (les plus anciens en premier)
    # On va récupérer les dates pour trier
    messages_with_date = []
    for msg in messages:
        try:
            msg_detail = service.users().messages().get(
                userId='me', 
                id=msg['id'], 
                format='metadata',
                metadataHeaders=['Date']
            ).execute()
            date_header = None
            for header in msg_detail.get('payload', {}).get('headers', []):
                if header.get('name') == 'Date':
                    date_header = header.get('value')
                    break
            messages_with_date.append((msg, date_header))
        except:
            messages_with_date.append((msg, None))
    
    # Trier du plus ancien au plus récent
    from email.utils import parsedate_to_datetime
    messages_with_date.sort(key=lambda x: parsedate_to_datetime(x[1]) if x[1] else datetime.now(), reverse=True)
    
    messages = [msg for msg, date in messages_with_date]

    emails = []
    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        emails.append(decode_message(msg_detail))

    return emails

def extract_actions(body, subject):
    """Extrait des actions potentielles d'un email"""
    import re
    
    actions = []
    
    # Mots-clés d'action français (plus restrictifs)
    action_keywords = [
        'à faire', 'à vérifier', 'merci de', 's\'il te plaît', 'svp',
        'urgent', 'deadline', 'échéance', 'répondre', 'confirmer',
        'faire', 'voir', 'regarder', 'vérifier', 'mettre à jour',
        'renvoyer', 'envoyer', 'appeler', 'contacter', 'prendre rendez-vous'
    ]
    
    # Mots-clés d'action anglais (plus restrictifs)
    action_keywords_en = [
        'please', 'urgent', 'deadline', 'due', 'reply', 'confirm',
        'send', 'call', 'contact', 'need to', 'should'
    ]
    
    all_keywords = action_keywords + action_keywords_en
    
    # Mots à ignorer (conditions juridiques, etc.)
    ignore_patterns = [
        r'^if ', r'^when ', r'^unless ', r'^you acknowledge', 
        r'^you may', r'^it will take', r'^we will', r'^we are'
    ]
    
    # Recherche dans le sujet
    for keyword in all_keywords:
        if keyword.lower() in subject.lower():
            actions.append(f"[⚠️ SUJET IMPORTANT] Contient '{keyword}'")
    
    # Recherche dans le corps - phrases avec mots-clés
    for keyword in all_keywords:
        pattern = rf'([^.?!]*{keyword}[^.?!]*[.?!])'
        matches = re.findall(pattern, body, re.IGNORECASE)
        for match in matches:
            # Nettoyer et limiter la longueur
            action = match.strip()
            
            # Ignorer les phrases qui commencent par des mots d'ignorance
            ignore = False
            for ignore_pattern in ignore_patterns:
                if re.match(ignore_pattern, action.lower()):
                    ignore = True
                    break
            
            if not ignore and len(action) > 10 and len(action) < 150:
                actions.append(f"• {action}")
    
    # Recherche de tâches explicites (tirets, points, etc.)
    lines = body.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith(('-', '*', '•', '1.', '2.', '3.', '4.', '5.')) and len(line) < 150:
            actions.append(f"[LISTE] {line[1:].strip()}")
    
    # Détection de demandes spécifiques
    requests = [
        r'peux[-tu]+ (.+)',
        r'pourrai[-tu]+ (.+)',
        r'pourrais[-tu]+ (.+)',
        r'pouvez[-vous]+ (.+)',
        r'pourriez[-vous]+ (.+)',
    ]
    
    for pattern in requests:
        matches = re.findall(pattern, body, re.IGNORECASE)
        for match in matches:
            action = match.strip()
            if len(action) > 10 and len(action) < 100:
                actions.append(f"[⚠️ DEMANDE] {action}")
    
    return actions

def summarize_emails(emails, mode='summary'):
    print(f"\n{'='*60}")
    print(f"📧 RÉSUMÉ EMAILS - {datetime.now().strftime('%d/%m/%Y')}")
    print(f"{'='*60}\n")

    total_actions = 0
    all_actions = []
    
    # Collecter toutes les actions avec priorité
    for i, email_data in enumerate(emails, 1):
        subject = email_data['subject'] or '(Pas de sujet)'
        sender = email_data['sender'] or '(Expéditeur inconnu)'
        
        actions = extract_actions(email_data['body'], subject)
        
        # Marquer les actions urgentes
        for action in actions:
            priority = 'HIGH' if '⚠️' in action else 'MEDIUM' if 'please' in action.lower() or 'merci de' in action.lower() else 'LOW'
            all_actions.append({
                'action': action,
                'subject': subject,
                'sender': sender,
                'priority': priority,
                'email_index': i
            })
        
        total_actions += len(actions)
    
    # Afficher le résumé
    print(f"📊 STATISTIQUES:")
    print(f"   Total emails: {len(emails)}")
    print(f"   Total actions: {total_actions}")
    print(f"   Emails avec actions: {len([e for e in emails if extract_actions(e['body'], e['subject'])])}")
    
    # Trier les actions par priorité
    priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    all_actions.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    # Afficher les actions par priorité
    if mode == 'summary':
        print(f"\n{'='*60}")
        print(f"⚡ ACTIONS PRIORITAIRES")
        print(f"{'='*60}\n")
        
        high_priority = [a for a in all_actions if a['priority'] == 'HIGH']
        medium_priority = [a for a in all_actions if a['priority'] == 'MEDIUM']
        
        if high_priority:
            print(f"🔴 URGENT ({len(high_priority)} actions):")
            for i, action_data in enumerate(high_priority[:10], 1):
                print(f"{i}. {action_data['action']}")
                print(f"   → {action_data['subject']}")
                print(f"   → {action_data['sender']}\n")
        
        if medium_priority:
            print(f"🟡 IMPORTANT ({len(medium_priority)} actions):")
            for i, action_data in enumerate(medium_priority[:5], 1):
                print(f"{i}. {action_data['action']}")
                print(f"   → {action_data['subject']}\n")
        
        low_count = len([a for a in all_actions if a['priority'] == 'LOW'])
        if low_count > 0:
            print(f"⚪ Autres: {low_count} actions à traiter")
    else:
        # Mode détaillé
        for i, email_data in enumerate(emails, 1):
            subject = email_data['subject'] or '(Pas de sujet)'
            sender = email_data['sender'] or '(Expéditeur inconnu)'
            
            print(f"\n{'─'*60}")
            print(f"{'📧 EMAIL ' + str(i)}")
            print(f"{'─'*60}")
            print(f"Sujet: {subject}")
            print(f"De: {sender}")
            
            actions = extract_actions(email_data['body'], subject)
            
            if actions:
                print(f"\n⚡ ACTIONS DÉTECTÉES ({len(actions)}):")
                for action in actions[:5]:
                    print(f"   • {action}")
                if len(actions) > 5:
                    print(f"   ... et {len(actions) - 5} autre(s)")
            else:
                print(f"\n   Aucune action détectée")
            
            # Aperçu du corps
            body_lines = [line.strip() for line in email_data['body'].split('\n') if line.strip()]
            if body_lines:
                preview_lines = body_lines[:3]
                preview = '\n   '.join(preview_lines)
                if len(body_lines) > 3:
                    preview += '\n   [...'
                print(f"\n📄 Aperçu:\n   {preview}")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    service = get_gmail_service()
    if service:
        emails = get_recent_emails(service, days=1, max_emails=15)
        summarize_emails(emails)
