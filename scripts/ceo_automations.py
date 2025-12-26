#!/usr/bin/env python3
"""
Script principal pour automatisations CEO - appelé par opencode
"""

import sys
import os
from datetime import datetime

def summarize_emails():
    """Résume les emails récents avec extraction d'actions"""
    try:
        from gmail_auth import get_gmail_service
        from summarize_emails import get_recent_emails, summarize_emails as format_emails
        
        print("\n📧 Récupération des emails depuis l'inbox...")
        service = get_gmail_service()
        
        if not service:
            print("❌ Erreur: Service Gmail non configuré")
            print("   Voir automatisations/gmail_setup.md pour la configuration")
            return
        
        emails = get_recent_emails(service, days=0)
        
        if not emails:
            print("Aucun email récent trouvé dans l'inbox.")
            return
        
        format_emails(emails, mode='summary')
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("   Assurez-vous d'avoir installé les dépendances:")
        print("   cd scripts && pip install -r requirements.txt")

def show_priorities():
    """Affiche les priorités actuelles"""
    try:
        with open('../priorites.md', 'r') as f:
            print("\n📋 PRIORITÉS ACTUELLES")
            print("="*60)
            print(f.read())
    except FileNotFoundError:
        print("\n❌ Fichier priorites.md non trouvé")

def weekly_checkin():
    """Génère le template de weekly check-in"""
    week = datetime.now().isocalendar()[1]
    template_path = f"../rapports/semaine_{week}.md"
    
    try:
        with open('../templates/weekly_checkin.md', 'r') as f:
            content = f.read()
            content = content.replace('Semaine [X]', f'Semaine {week}')
            
        with open(template_path, 'w') as f:
            f.write(content)
            
        print(f"\n✅ Template créé: {template_path}")
        print("   Éditez-le pour remplir votre check-in hebdomadaire")
        
    except FileNotFoundError:
        print("\n❌ Template non trouvé")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nCommandes disponibles:")
        print("  emails    - Résume les emails récents")
        print("  priorites - Affiche les priorités actuelles")
        print("  checkin   - Crée le weekly check-in template")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "emails":
        summarize_emails()
    elif command == "priorites":
        show_priorities()
    elif command == "checkin":
        weekly_checkin()
    else:
        print(f"Commande inconnue: {command}")
