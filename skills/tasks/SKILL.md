---
name: tasks
description: Gère les tâches et issues GitHub via le script github_manager.py. Crée, liste et suit les issues pour les projets PETITJEAN et WEMEDIA. Utilise ce skill quand l'utilisateur demande de créer une issue, lister les tâches, ou gérer le suivi des projets.
---

# Gestion des Tâches et Issues GitHub

## Objectif
Gérer les tâches et issues GitHub pour les projets PETITJEAN et WEMEDIA via le script `github_manager.py`.

## Prérequis

Le script nécessite un token GitHub configuré :
```bash
export GITHUB_TOKEN="votre_token_ici"
```

Ou définir le token dans un fichier `.env` à la racine du projet.

## Commandes disponibles

### Créer une issue
Crée une nouvelle issue GitHub avec les métadonnées standards.

**Syntaxe :**
```bash
python3 scripts/github_manager.py --create \
  --repo ceo-management \
  --initials DP \
  --title "Titre de la tâche" \
  --description "Description détaillée" \
  --priority Urgent \
  --entity PETITJEAN
```

**Paramètres :**
- `--repo` : Nom du dépôt (requis)
- `--initials` : Initiales du créateur (requis)
- `--title` : Titre de la tâche (requis)
- `--description` : Description détaillée (optionnel, défaut: "")
- `--priority` : Priorité - Urgent, Normal, Low (optionnel, défaut: Normal)
- `--entity` : Entité - PETITJEAN ou WEMEDIA (optionnel)

**Exemple :**
```bash
python3 scripts/github_manager.py --create \
  --repo ceo-management \
  --initials DP \
  --title "Problème de reprise de matériel" \
  --description "## Contexte
Description du problème...

## Impact
- Point 1
- Point 2" \
  --priority Urgent \
  --entity PETITJEAN
```

**Avec description multi-ligne :**
```bash
python3 scripts/github_manager.py --create \
  --repo ceo-management \
  --initials DP \
  --title "Bug critique" \
  --description "$(cat <<'EOF'
## Contexte
Description détaillée...

## Impact
- Point 1
- Point 2
EOF
)" \
  --priority Urgent \
  --entity PETITJEAN
```

### Lister les issues
Liste toutes les issues d'un dépôt avec filtres optionnels.

**Syntaxe de base :**
```bash
python3 scripts/github_manager.py --list --repo ceo-management
```

**Avec filtres :**
```bash
# Filtrer par initiales
python3 scripts/github_manager.py --list --repo ceo-management --filter-initials DP

# Filtrer par entité
python3 scripts/github_manager.py --list --repo ceo-management --filter-entity PETITJEAN

# Lister les issues fermées
python3 scripts/github_manager.py --list --repo ceo-management --status closed

# Lister toutes les issues (ouvertes et fermées)
python3 scripts/github_manager.py --list --repo ceo-management --status all
```

**Paramètres :**
- `--list` : Active le mode liste (requis)
- `--repo` : Nom du dépôt (optionnel, liste tous les dépôts si omis)
- `--filter-initials` : Filtrer par initiales (optionnel)
- `--filter-entity` : Filtrer par entité - PETITJEAN ou WEMEDIA (optionnel)
- `--status` : Statut - open, closed, all (optionnel, défaut: open)

### Mettre à jour une issue
Met à jour une issue existante (labels, commentaires).

**Syntaxe :**
```bash
python3 scripts/github_manager.py --update \
  --repo ceo-management \
  --issue 42 \
  --add-label "En cours" \
  --comment "Mise à jour du statut"
```

**Paramètres :**
- `--update` : Active le mode mise à jour (requis)
- `--repo` : Nom du dépôt (requis)
- `--issue` : Numéro de l'issue (requis)
- `--add-label` : Ajouter un label (peut être répété plusieurs fois)
- `--comment` : Ajouter un commentaire (optionnel)

**Exemple :**
```bash
python3 scripts/github_manager.py --update \
  --repo ceo-management \
  --issue 42 \
  --add-label "Review" \
  --comment "Prêt pour revue"
```

### Fermer une issue
Ferme une issue (équivalent à suppression pour les workflows).

**Syntaxe :**
```bash
python3 scripts/github_manager.py --close \
  --repo ceo-management \
  --issue 42 \
  --comment "Tâche terminée"
```

**Paramètres :**
- `--close` : Ferme l'issue (requis)
- `--repo` : Nom du dépôt (requis)
- `--issue` : Numéro de l'issue (requis)
- `--comment` : Commentaire de fermeture (optionnel)

**Exemple :**
```bash
python3 scripts/github_manager.py --close \
  --repo ceo-management \
  --issue 42 \
  --comment "Résolu et déployé en production"
```

## Convention de nommage

Toutes les issues doivent suivre le format : `[INITIALES] Titre`

Exemples :
- `[DP] Problème de reprise de matériel`
- `[MP] Mettre à jour la documentation`
- `[CT] Refactoriser le système de paiement`

## Priorités

Les priorités disponibles sont (de la plus haute à la plus basse) :
1. **Urgent** - Bloquant ou critique
2. **Normal** - Standard
3. **Low** - Peut attendre

## Statuts

Les statuts de workflow sont :
1. **Todo** - À faire
2. **In Progress** - En cours
3. **Review** - En revue
4. **Done** - Terminé

## Entités

- **PETITJEAN** - Tâches liées à l'entreprise PETITJEAN
- **WEMEDIA** - Tâches liées à l'agence WEMEDIA

## Dépôts disponibles

- `ceo-management` - Management général CEO

## Workflow pour OpenCode

Quand l'utilisateur demande de créer une tâche/issue :

1. Collecter les informations nécessaires :
   - Titre de la tâche
   - Description détaillée (avec contexte, problème, impact, solution)
   - Priorité (Urgent, Normal, Low)
   - Entité (PETITJEAN ou WEMEDIA)
   - Initiales du créateur (défaut : DP pour Damien Petitjean)

2. Exécuter la commande en ligne de commande pour créer l'issue :
   ```bash
   python3 scripts/github_manager.py --create --repo ceo-management --initials DP --title "..." --description "..." --priority Urgent --entity PETITJEAN
   ```

3. Afficher le lien vers l'issue créée (affiché automatiquement par le script)

Quand l'utilisateur demande de lister les tâches :

1. Exécuter la commande de liste avec les filtres appropriés :
   ```bash
   python3 scripts/github_manager.py --list --repo ceo-management
   ```

2. Présenter les résultats de manière structurée (affichés automatiquement par le script)

3. Filtrer par priorité/statut/entité si demandé en ajoutant les options `--filter-entity`, `--filter-initials`, `--status`

Quand l'utilisateur demande de modifier une tâche :

1. Utiliser la commande `--update` avec le numéro de l'issue
2. Ajouter des labels ou commentaires selon les besoins

Quand l'utilisateur demande de supprimer/fermer une tâche :

1. Utiliser la commande `--close` avec le numéro de l'issue
2. Optionnellement ajouter un commentaire de fermeture

## Messages clés

### Messages à afficher
- "✅ Issue créée : [URL]"
- "📋 Issues trouvées : X"
- "✅ Issue mise à jour"

### Messages d'erreur
- "❌ GITHUB_TOKEN non trouvé. Exportez-le : export GITHUB_TOKEN='votre_token'"
- "❌ Impossible de créer l'issue : [erreur]"
- "❌ Dépôt introuvable : [nom]"

## Exemples d'utilisation

### Exemple 1 : Créer une issue urgente
```bash
python3 scripts/github_manager.py --create \
  --repo ceo-management \
  --initials DP \
  --title "Bug critique sur le site" \
  --description "Le site est inaccessible depuis 10h." \
  --priority Urgent \
  --entity PETITJEAN
```

### Exemple 2 : Créer une issue avec description multi-ligne
```bash
python3 scripts/github_manager.py --create \
  --repo ceo-management \
  --initials DP \
  --title "Refonte du système de paiement" \
  --description "$(cat <<'EOF'
## Contexte
Le système actuel ne supporte plus les nouvelles réglementations.

## Impact
- Non-conformité légale
- Risque d'amende

## Solution proposée
Migration vers Stripe Connect
EOF
)" \
  --priority Normal \
  --entity WEMEDIA
```

### Exemple 3 : Lister toutes les issues ouvertes
```bash
python3 scripts/github_manager.py --list --repo ceo-management
```

### Exemple 4 : Lister les issues d'une personne spécifique
```bash
python3 scripts/github_manager.py --list \
  --repo ceo-management \
  --filter-initials DP
```

### Exemple 5 : Lister les issues d'une entité
```bash
python3 scripts/github_manager.py --list \
  --repo ceo-management \
  --filter-entity PETITJEAN
```

### Exemple 6 : Mettre à jour une issue (ajouter un label)
```bash
python3 scripts/github_manager.py --update \
  --repo ceo-management \
  --issue 42 \
  --add-label "In Progress"
```

### Exemple 7 : Ajouter un commentaire à une issue
```bash
python3 scripts/github_manager.py --update \
  --repo ceo-management \
  --issue 42 \
  --comment "Début du travail sur cette tâche"
```

### Exemple 8 : Fermer une issue
```bash
python3 scripts/github_manager.py --close \
  --repo ceo-management \
  --issue 42 \
  --comment "Tâche terminée et déployée"
```

## Structure des issues

Une issue GitHub créée contient :

```markdown
## Description
[Description de la tâche]

## Métadonnées
- **Priorité**: Urgent/Normal/Low
- **Entité**: PETITJEAN/WEMEDIA
- **Créateur**: [INITIALES]
- **Date**: [DATE]
- **Assigné à**: [USERNAME]
```