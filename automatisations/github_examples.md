# Exemples d'utilisation du GitHub Manager

Voici quelques exemples concrets d'utilisation des scripts de gestion GitHub.

## 1. Voir toutes mes issues en cours

```bash
cd scripts && python3 github_manager.py --list --filter-initials DP
```

Résultat attendu :
```
📋 3 issue(s) trouvée(s):

[bricov4] #42: [DP] Fix bug login
  URL: https://github.com/ddpetit/bricov4/issues/42
  Labels: Urgent, PETITJEAN

[supernestor] #15: [DP] Implementer JWT auth
  URL: https://github.com/ddpetit/supernestor/issues/15
  Labels: Normal, WEMEDIA

[comparat] #28: [DP] Optimiser base de données
  URL: https://github.com/ddpetit/comparat/issues/28
  Labels: Normal, WEMEDIA
```

## 2. Créer une nouvelle issue

```bash
cd scripts && python3 github_manager.py --create --repo supernestor --initials DP --title "Fix bug API" --description "L'API renvoie une erreur 500" --priority "Urgent" --entity "WEMEDIA"
```

Résultat attendu :
```
✅ Issue créée: https://github.com/ddpetit/supernestor/issues/16
```

## 3. Voir toutes les issues WEMEDIA

```bash
cd scripts && python3 github_manager.py --list --filter-entity WEMEDIA
```

## 4. Fermer une issue terminée

```bash
cd scripts && python3 github_manager.py --close 42 --repo bricov4 --comment "Bug corrigé, testé et validé"
```

## 5. Générer un rapport hebdomadaire

```bash
cd scripts && python3 github_manager.py --report --output rapports/projets_semaine_52.md
```

## 6. Importer un lot de tâches

D'abord, créer un fichier `tasks.json` :
```json
[
  {
    "initials": "DP",
    "title": "Configurer l'authentification JWT",
    "description": "Implémenter l'authentification JWT pour l'API",
    "priority": "Urgent"
  },
  {
    "initials": "ML",
    "title": "Optimiser les requêtes base de données",
    "description": "Ajouter des index et optimiser les requêtes lentes",
    "priority": "Normal"
  }
]
```

Puis importer :
```bash
cd scripts && python3 github_manager.py --import tasks.json --repo supernestor --entity WEMEDIA
```

## 7. Mettre à jour le statut d'une issue

```bash
cd scripts && python3 github_manager.py --update --issue 42 --repo bricov4 --add-label "In Progress"
```

## Usage quotidien recommandé

**Matin (15 min)** :
```bash
# Voir mes priorités
cat ../priorites.md

# Voir mes issues en cours
cd scripts && python3 github_manager.py --list --filter-initials DP
```

**Lundi (30 min)** :
```bash
# Rapport hebdomadaire
cd scripts && python3 github_manager.py --report

# Weekly check-in
cd scripts && python3 ../automatisations/ceo_automations.py checkin
```

## Intégration avec opencode

Vous pouvez me demander directement :
- "Crée une issue pour supernestor : Fix bug login"
- "Montre-moi mes issues en cours"
- "Ferme l'issue #42 sur bricov4"
- "Génère un rapport projets"

Je gérerai les commandes pour vous !