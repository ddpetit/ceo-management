---
name: daily-checkin
description: Effectue un checkin quotidien interactif qui récupère les emails Gmail, analyse les urgents et importants, et pose des questions à l'utilisateur pour définir les tâches du jour. Utilise ce skill quand l'utilisateur demande un checkin quotidien ou résumé des emails.
---

# Daily Check-in Interactif

## Objectif
Effectuer un checkin quotidien interactif qui récupère tous les emails de l'inbox Gmail, les analyse pour identifier les urgents et importants, puis pose des questions à l'utilisateur pour définir les tâches du jour.

## Workflow pour OpenCode

### Étape 1: Récupérer et analyser les emails
Exécuter ce script Python pour créer le fichier JSON de checkin:

```bash
python3 <<'PYTHON_EOF'
import sys
sys.path.insert(0, 'scripts')
from gmail_auth import get_gmail_service
from summarize_emails import get_recent_emails, extract_actions
import json
from datetime import datetime, date
from pathlib import Path

LOG_DIR = Path('logs/daily_checkins')
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"{date.today().strftime('%Y-%m-%d')}.json"

service = get_gmail_service()
emails = get_recent_emails(service, days=0)

def analyze_importance(email):
    subject = email['subject'] or ''
    body = email['body'] or ''
    
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

important_emails = []
for email in emails:
    importance, actions = analyze_importance(email)
    if importance in ['HIGH', 'MEDIUM']:
        important_emails.append({
            'subject': email['subject'],
            'sender': email['sender'],
            'importance': importance,
            'actions': actions
        })

high_priority = [e for e in important_emails if e['importance'] == 'HIGH']
medium_priority = [e for e in important_emails if e['importance'] == 'MEDIUM']

data = {
    'date': date.today().strftime('%Y-%m-%d'),
    'timestamp': datetime.now().isoformat(),
    'emails': {
        'total': len(emails),
        'high_priority': len(high_priority),
        'medium_priority': len(medium_priority),
        'high_priority_emails': high_priority,
        'medium_priority_emails': medium_priority
    },
    'tasks': []
}

with open(LOG_FILE, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ {len(emails)} emails analysés et sauvegardés")
PYTHON_EOF
```

Ce script:
- Se connecte à Gmail via l'API (utilise `gmail_auth.py`)
- Récupère tous les emails de l'inbox (utilise `summarize_emails.py`)
- Analyse l'importance des emails
- Classe en HIGH (urgents), MEDIUM (importants), LOW (faible)
- Sauvegarde les résultats dans `logs/daily_checkins/YYYY-MM-DD.json`

### Étape 2: Lire le fichier de checkin
Lire le fichier JSON du jour:
```
logs/daily_checkins/YYYY-MM-DD.json
```

### Étape 3: Présenter un résumé à l'utilisateur

#### Afficher les statistiques
- Total emails
- Nombre d'urgents
- Nombre d'importants

#### Afficher les emails URGENTS (HIGH priority)
Pour chaque email urgent:
- Sujet
- Expéditeur
- Actions détectées (si disponibles, limiter à 2-3)

#### Afficher les emails IMPORTANTS (MEDIUM priority)
Afficher les 15-20 emails les plus importants avec:
- Sujet
- Expéditeur

#### Groupement suggéré
- Fournisseurs (Kubota, Tama, Cosnet, etc.)
- Clients
- Internes

### Étape 4: Poser des questions à l'utilisateur

Poser cette question:
```
✨ Quelles sont tes tâches pour aujourd'hui ?

Format: Tâche|Priorité
Priorités: H (Urgent), M (Moyen), L (Faible)

Exemples:
- Appeler Nicolas Barras lundi à 13H|H
- Aider Sabrina pour Weldom|M
- Répondre à KUBOTA|M

Tape tes tâches (une par ligne) et termine par "fin"
```

Attendre les réponses de l'utilisateur et les collecter.

### Étape 5: Sauvegarder les tâches
Mettre à jour le fichier JSON avec les tâches collectées dans la propriété `tasks`:

```json
{
  "tasks": [
    {
      "task": "Nom de la tâche",
      "priority": "HIGH|MEDIUM|LOW",
      "status": "TODO"
    }
  ]
}
```

### Étape 6: Afficher le résumé final
Afficher un résumé des tâches sauvegardées avec des emojis:
- 🔴 HIGH
- 🟡 MEDIUM
- ⚪ LOW

## Scripts disponibles

Ce skill utilise les scripts partagés dans `scripts/`:

- `scripts/gmail_auth.py` - Authentification Gmail API
- `scripts/summarize_emails.py` - Récupération et analyse des emails

Ces scripts sont utilisés via le script inline Python dans "Étape 1".

## Structure des données

### Fichier JSON de checkin
```json
{
  "date": "2025-12-26",
  "timestamp": "2025-12-26T14:26:54.598106",
  "emails": {
    "total": 90,
    "yesterday": 0,
    "diff": 90,
    "high_priority": 7,
    "medium_priority": 59,
    "high_priority_emails": [
      {
        "subject": "Sujet de l'email",
        "sender": "expediteur@email.com",
        "actions": ["action 1", "action 2"]
      }
    ],
    "medium_priority_emails": [
      {
        "subject": "Sujet de l'email",
        "sender": "expediteur@email.com"
      }
    ]
  },
  "tasks": [
    {
      "task": "Description de la tâche",
      "priority": "HIGH|MEDIUM|LOW",
      "status": "TODO"
    }
  ]
}
```

## Améliorations possibles

### Court terme
- [ ] Ajouter la détection de catégories (fournisseurs, clients, internes)
- [ ] Améliorer l'extraction d'actions des emails
- [ ] Filtrer les forwards et duplicats
- [ ] Ajouter un résumé textuel des emails

### Moyen terme
- [ ] Intégration avec la gestion de tâches existante
- [ ] Historique et statistiques sur les checkins
- [ ] Suggestions de tâches basées sur les emails
- [ ] Détection automatique des tâches récurrentes

### Long terme
- [ ] Analyse avec IA pour classer et résumer les emails
- [ ] Suggestion de priorités automatiques
- [ ] Intégration avec un calendrier
- [ ] Rapports hebdomadaires/mensuels

## Exécution du skill par OpenCode

Quand l'utilisateur demande "Peux-tu me faire le checkin quotidien ?":

1. Exécuter le script Python inline de "Étape 1" pour récupérer les emails
2. Lire le fichier JSON du jour avec `read` tool
3. Présenter un résumé structuré:
   - Statistiques
   - Emails urgents (avec actions)
   - Emails importants (top 15-20)
4. Poser la question: "Quelles sont tes tâches pour aujourd'hui ?"
5. Donner le format et des exemples
6. Attendre les réponses de l'utilisateur (ne pas exécuter automatiquement)
7. Collecter les tâches et les sauvegarder dans le fichier JSON avec `edit` tool
8. Afficher le résumé final

## Messages clés

### Messages à afficher
- "🌅 Daily Check-in - [DATE]"
- "📊 Statistiques: Total emails: X, Urgents: Y, Importants: Z"
- "🔴 Emails URGENTS (X)"
- "🟡 Emails IMPORTANTS (X - Top 15)"
- "✨ Quelles sont tes tâches pour aujourd'hui ?"
- "Format: Tâche|Priorité (H=Urgent, M=Moyen, L=Faible)"
- "✅ X tâche(s) sauvegardée(s)"
- "📋 RÉSUMÉ FINAL"

### Messages d'erreur
- "❌ Aucun checkin trouvé pour aujourd'hui"
- "Erreur: impossible de se connecter à Gmail"
