#!/usr/bin/env python3
import json
import os
from datetime import datetime, date, timedelta
from pathlib import Path
from gmail_auth import get_gmail_service
from summarize_emails import get_recent_emails, extract_actions

LOG_DIR = Path(__file__).parent.parent / 'logs'
DAILY_CHECKIN_DIR = LOG_DIR / 'daily_checkins'
STATS_FILE = LOG_DIR / 'email_stats.json'

def load_stats():
    if STATS_FILE.exists():
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_stats(stats):
    LOG_DIR.mkdir(exist_ok=True)
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2, default=str)

def get_date_key():
    return date.today().strftime('%Y-%m-%d')

def get_yesterday_key():
    yesterday = date.today() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def analyze_importance(email):
    """Détermine l'importance d'un email"""
    subject = email['subject'] or ''
    body = email['body'] or ''
    sender = email['sender'] or ''
    
    actions = extract_actions(body, subject)
    has_actions = len(actions) > 0
    has_urgent = any('urgent' in a.lower() or 'deadline' in a.lower() or 'échéance' in a.lower() for a in actions)
    
    high_priority_keywords = ['urgent', 'deadline', 'échéance', 'asap', 'important', 'priority']
    medium_priority_keywords = ['merci de', 'please', 'svp', 'confirmation', 'réponse']
    
    subject_lower = subject.lower()
    body_lower = body.lower()
    
    importance = 'LOW'
    if has_urgent or any(kw in subject_lower or kw in body_lower for kw in high_priority_keywords):
        importance = 'HIGH'
    elif has_actions or any(kw in subject_lower or kw in body_lower for kw in medium_priority_keywords):
        importance = 'MEDIUM'
    
    return importance, actions

def run_checkin():
    print("\n" + "="*70)
    print("🌅 DAILY CHECK-IN")
    print("="*70)
    print(f"📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    
    service = get_gmail_service()
    if not service:
        print("❌ Erreur: Impossible de se connecter à Gmail")
        return
    print(f"✅ Service Gmail connecté")
    
    print("📧 Récupération des emails...")
    emails = get_recent_emails(service, days=0)
    total_emails = len(emails)
    
    stats = load_stats()
    today_key = get_date_key()
    yesterday_key = get_yesterday_key()
    
    yesterday_count = 0
    if yesterday_key in stats:
        yesterday_count = stats[yesterday_key]['total_emails']
    
    diff = total_emails - yesterday_count
    diff_text = ""
    if diff > 0:
        diff_text = f"📈 +{diff}"
    elif diff < 0:
        diff_text = f"📉 {diff}"
    else:
        diff_text = "➡️ ="
    
    stats[today_key] = {
        'total_emails': total_emails,
        'timestamp': datetime.now().isoformat()
    }
    save_stats(stats)
    
    print(f"\n📊 STATISTIQUES EMAILS")
    print(f"   Aujourd'hui: {total_emails} emails")
    print(f"   Hier: {yesterday_count} emails")
    print(f"   Évolution: {diff_text}")
    
    important_emails = []
    for email in emails:
        importance, actions = analyze_importance(email)
        if importance in ['HIGH', 'MEDIUM']:
            important_emails.append({
                **email,
                'importance': importance,
                'actions': actions
            })
    
    high_priority = [e for e in important_emails if e['importance'] == 'HIGH']
    medium_priority = [e for e in important_emails if e['importance'] == 'MEDIUM']
    
    print(f"\n{'='*70}")
    print(f"🔴 EMAILS URGENTS ({len(high_priority)})")
    print(f"{'='*70}")
    for i, email in enumerate(high_priority, 1):
        print(f"\n{i}. {email['subject']}")
        print(f"   De: {email['sender']}")
        if email['actions']:
            print(f"   Actions:")
            for action in email['actions'][:3]:
                print(f"      • {action}")
    
    print(f"\n{'='*70}")
    print(f"🟡 EMAILS IMPORTANTS ({len(medium_priority)})")
    print(f"{'='*70}")
    for i, email in enumerate(medium_priority[:5], 1):
        print(f"\n{i}. {email['subject']}")
        print(f"   De: {email['sender']}")
    
    checkin_data = {
        'date': today_key,
        'timestamp': datetime.now().isoformat(),
        'emails': {
            'total': total_emails,
            'yesterday': yesterday_count,
            'diff': diff,
            'high_priority': len(high_priority),
            'medium_priority': len(medium_priority),
            'high_priority_emails': [
                {
                    'subject': e['subject'],
                    'sender': e['sender'],
                    'actions': e['actions']
                }
                for e in high_priority
            ],
            'medium_priority_emails': [
                {
                    'subject': e['subject'],
                    'sender': e['sender']
                }
                for e in medium_priority
            ]
        },
        'tasks': []
    }
    
    return checkin_data

def log_tasks(checkin_data, tasks):
    checkin_data['tasks'] = tasks
    
    DAILY_CHECKIN_DIR.mkdir(parents=True, exist_ok=True)
    today_key = get_date_key()
    log_file = DAILY_CHECKIN_DIR / f"{today_key}.json"
    
    with open(log_file, 'w') as f:
        json.dump(checkin_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Checkin sauvegardé dans {log_file}")
    
    print(f"\n{'='*70}")
    print(f"📋 RÉSUMÉ DES TÂCHES")
    print(f"{'='*70}")
    for i, task in enumerate(tasks, 1):
        priority_emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '⚪'}
        print(f"{i}. {priority_emoji[task['priority']]} {task['task']}")
    
    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    import sys
    
    checkin_data = run_checkin()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--tasks':
        tasks = []
        for task_input in sys.argv[2:]:
            parts = task_input.split('|')
            task = parts[0].strip()
            priority = parts[1].strip().upper() if len(parts) > 1 else 'MEDIUM'
            priority_map = {'H': 'HIGH', 'M': 'MEDIUM', 'B': 'LOW'}
            priority = priority_map.get(priority, 'MEDIUM')
            tasks.append({
                'task': task,
                'priority': priority,
                'status': 'TODO'
            })
        log_tasks(checkin_data, tasks)
    elif checkin_data:
        print(f"\n{'='*70}")
        print(f"✅ TÂCHES DU JOUR")
        print(f"{'='*70}")
        
        tasks = []
        while True:
            try:
                task = input("\nEntrez une tâche (ou 'fin' pour terminer): ").strip()
                if task.lower() in ['fin', 'done', '']:
                    break
                priority = input("Priorité (H/M/B)? [M] ").strip().upper() or 'M'
                priority_map = {'H': 'HIGH', 'M': 'MEDIUM', 'B': 'LOW'}
                priority = priority_map.get(priority, 'MEDIUM')
                tasks.append({
                    'task': task,
                    'priority': priority,
                    'status': 'TODO'
                })
            except EOFError:
                break
        
        log_tasks(checkin_data, tasks)
