# Espace CEO - PETITJEAN & WEMEDIA

## 📁 Structure

### Entreprises
- `PETITJEAN/` - Documentation, processus, stratégie, KPIs
- `WEMEDIA/` - Documentation, processus, stratégie, KPIs

### Gestion
- `reunions/` - Comptes-rendus et agendas
- `finances/` - Budgets, factures, rapports
- `projets/` - Roadmaps et suivi

### Suivi personnel
- `priorites.md` - Gestion quotidienne des priorités
- `objectifs/` - OKRs et KPIs tracking
- `templates/` - Modèles réutilisables

### Automatisations
- `scripts/` - Scripts Python pour automatiser
- `automatisations/` - Config et docs

## 🚀 Quick Start

### Installation des dépendances
```bash
cd scripts
pip install -r requirements.txt
```

### Configuration GitHub
Créez un token GitHub avec les permissions `repo` et exportez-le :
```bash
export GITHUB_TOKEN=votre_token_ici
```

## 📋 Gestion des Projets

### GitHub Projects

Utilisez l'onglet **Projects** de ce dépôt pour gérer tous les projets PETITJEAN et WEMEDIA.

**Convention de nommage des issues** :
`[INITIALES] Description de la tâche`

Exemples :
- `[DP] Fix bug login`
- `[ML] Refactor API`
- `[JS] Configurer CI/CD`

**Champs personnalisés** :
- `Assigné à` : Liste des employés
- `Projet` : bricov4, supernestor, comparat, comparem, zagrow, my_zagrow
- `Entité` : WEMEDIA, PETITJEAN
- `Priorité` : Urgent, Normal, Low
- `Statut` : Todo, In Progress, Review, Done

### Scripts de gestion GitHub

**Créer une issue** :
```bash
cd scripts && python github_manager.py --create --repo supernestor --initials DP --title "Fix bug login"
```

**Voir mes issues** :
```bash
cd scripts && python github_manager.py --list --filter-initials DP
```

**Générer un rapport** :
```bash
cd scripts && python github_manager.py --report
```

Pour plus de commandes, voir `COMMANDES.md`

**Workflow** :
1. Créez une issue dans le dépôt technique approprié
2. Ajoutez-la au GitHub Projects de ce dépôt
3. Suivez l'avancement dans le tableau kanban

## 📧 Automatisations Gmail

**Résumé des emails** :
```bash
cd scripts && python ceo_automations.py emails
```

Pour la configuration Gmail, voir `automatisations/gmail_setup.md`

## 📈 Workflow Hebdomadaire

**Lundi**
- Weekly check-in : `python ceo_automations.py checkin`
- Rapport projets : `python github_manager.py --report`
- Définir priorités de la semaine

**Mercredi**
- Review mi-semaine
- Ajuster priorités si nécessaire

**Vendredi**
- Réalisations de la semaine
- Planifier semaine suivante
- Review avancement projets
