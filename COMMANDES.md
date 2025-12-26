# 🚀 Commandes Opencode pour CEO

Vous pouvez utiliser ces commandes directement depuis l'interface opencode :

## 📧 Résumé Emails
```bash
cd scripts && python ceo_automations.py emails
```
Récupère et affiche les 10 derniers emails de Gmail

## 📋 Voir Priorités
```bash
cd scripts && python ceo_automations.py priorites
```
Affiche le contenu de `priorites.md`

## ✅ Weekly Check-in
```bash
cd scripts && python ceo_automations.py checkin
```
Crée un nouveau template dans `rapports/semaine_X.md`

## 🔧 GitHub Projects Management

### Créer une issue
```bash
cd scripts && python3 github_manager.py --create --repo supernestor --initials DP --title "Fix bug login" --description "Problème de connexion" --priority "Urgent" --entity "WEMEDIA"
```

### Lister les issues
```bash
# Toutes les issues ouvertes
cd scripts && python3 github_manager.py --list

# Par dépôt
cd scripts && python3 github_manager.py --list --repo supernestor

# Par employé (initiales)
cd scripts && python3 github_manager.py --list --filter-initials DP

# Par entité
cd scripts && python3 github_manager.py --list --filter-entity WEMEDIA

# Issues fermées
cd scripts && python3 github_manager.py --list --status closed
```

### Mettre à jour une issue
```bash
# Fermer une issue
cd scripts && python3 github_manager.py --close --issue 123 --repo supernestor --comment "Tâche terminée"

# Ajouter un label
cd scripts && python3 github_manager.py --update --issue 123 --repo supernestor --add-label "In Progress"

# Ajouter un commentaire
cd scripts && python3 github_manager.py --update --issue 123 --repo supernestor --comment "En cours de développement"
```

### Générer un rapport
```bash
cd scripts && python3 github_manager.py --report --output rapports/projets.md
```

### Importer des tâches depuis un fichier
```bash
cd scripts && python3 github_manager.py --import tasks.json --repo supernestor --entity WEMEDIA
```

### Gestion des tâches pendant la journée
```bash
# Voir le statut
python3 scripts/task_manager.py status

# Mettre à jour le statut d'une tâche
python3 scripts/task_manager.py update

# Ajouter une nouvelle tâche
python3 scripts/task_manager.py add
```

## 🎯 Workflow quotidien

**Matin**
1. Daily Checkin
2. `python3 github_manager.py --list --filter-initials DP` - Voir mes issues en cours
3. Mettre à jour `priorites.md`

**Pendant la journée**
- `python3 scripts/task_manager.py status` - Voir progression
- `python3 scripts/task_manager.py update` - Faire avancer les tâches

**Lundi**
- `python3 ceo_automations.py checkin` - Démarrer le weekly check-in
- `python3 github_manager.py --report` - Générer rapport projets
- Remplir `rapports/semaine_X.md`

**Vendredi**
- Finaliser le weekly check-in
- Planifier la semaine suivante
- Review du rapport projets

## ⚡ Rapide

Je peux exécuter ces commandes pour vous. Dites-moi simplement :
- "checkin" pour le daily checkin complet (emails + tâches)
- "status" ou "tâches" pour voir l'avancement du jour
- "mise à jour" pour faire avancer vos tâches
- "résumé emails" pour voir les emails
- "voir priorités" pour afficher vos priorités
- "weekly checkin" pour créer un rapport hebdomadaire
- "mes issues" pour voir vos issues en cours
- "créer issue" pour créer une nouvelle issue
- "rapport projets" pour générer le rapport
