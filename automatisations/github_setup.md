# Configuration GitHub

## Création d'un Token GitHub

1. Allez sur https://github.com/settings/tokens
2. Cliquez sur "Generate new token" → "Generate new token (classic)"
3. Donnez un nom (ex: "CEO Management")
4. Sélectionnez les permissions suivantes :
   - ✅ `repo` (accès complet aux dépôts)
   - ✅ `repo:status` (statut des commits)
   - ✅ `repo_deployment` (déploiement)
   - ✅ `public_repo` (dépôts publics)
   - ✅ `read:org` (lecture org)
5. Cliquez sur "Generate token"
6. **IMPORTANT** : Copiez le token immédiatement (il ne sera plus affiché)

## Configuration de l'environnement

### Méthode 1 : Variable d'environnement temporaire
```bash
export GITHUB_TOKEN=votre_token_ici
```

### Méthode 2 : Ajouter au .bashrc ou .zshrc (permanent)
```bash
echo 'export GITHUB_TOKEN=votre_token_ici' >> ~/.bashrc
source ~/.bashrc
```

### Méthode 3 : Créer un fichier .env
```bash
cd scripts
echo 'GITHUB_TOKEN=votre_token_ici' > .env
```

Puis modifier `github_manager.py` pour charger les variables depuis .env :
```python
from dotenv import load_dotenv
load_dotenv()
```

## Test de configuration

Testez que tout fonctionne :
```bash
cd scripts && python github_manager.py --list
```

Cela devrait afficher toutes les issues ouvertes de vos dépôts.

## Sécurité

⚠️ **IMPORTANT** :
- Ne commitez jamais votre token GitHub
- Le fichier `.env` est déjà dans `.gitignore`
- Changez votre token régulièrement
- Si un token est compromis, révoquez-le immédiatement dans les paramètres GitHub