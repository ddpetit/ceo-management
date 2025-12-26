# Configuration Automatisations Gmail

## 📧 Installation Gmail API

### 1. Créer un projet Google Cloud
1. Allez sur https://console.cloud.google.com/
2. Créez un nouveau projet
3. Activez l'API Gmail dans "APIs & Services > Library"

### 2. Créer les identifiants OAuth
1. "APIs & Services > Credentials"
2. "Create Credentials > OAuth client ID"
3. Choisissez "Desktop application"
4. Téléchargez le fichier JSON et renommez-le `credentials.json`
5. Placez-le dans `scripts/`

### 3. Installer les dépendances
```bash
pip install --upgrade google-api-python-client google-auth-oauthlib
```

### 4. Première utilisation
```bash
cd scripts
python summarize_emails.py
```

Un navigateur s'ouvrira pour autoriser l'accès à votre compte Gmail.

## 🤖 Résumé intelligent avec IA (optionnel)

Pour avoir un résumé avec extraction des points clés:

1. Ajoutez votre clé OpenAI dans `.env`:
```
OPENAI_API_KEY=votre_clé_ici
```

2. Le script peut être amélioré pour:
- Extraire les actions requises
- Identifier les emails prioritaires
- Catégoriser par thème (finances, équipe, clients...)
