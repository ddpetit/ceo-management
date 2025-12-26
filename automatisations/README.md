# Automatisations CEO

## Scripts disponibles

### Résumé emails (Gmail)
```bash
# Installation
cd scripts && pip install -r requirements.txt

# Configuration (voir automatisations/gmail_setup.md)

# Utilisation quotidienne
python scripts/summarize_emails.py
```

### Weekly report auto
```bash
python scripts/generate_weekly_report.py
```

## À mettre en place

1. **Résumé emails quotidien**
   - Script Python + API OpenAI
   - Lancer chaque matin

2. **Génération rapport hebdo**
   - Auto-fill depuis KPIs et priorités
   - Export PDF

3. **Rappels automatiques**
   - Notifications tâches prioritaires
   - Alertes KPIs en baisse

## Documentation API nécessaires
- Email provider (Gmail API, Outlook...)
- OpenAI API (résumés)
