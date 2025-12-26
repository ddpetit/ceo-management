# 🛠️ Guide: Ajouter de Nouvelles Commandes Personnalisées

## Structure Actuelle

Les commandes personnalisées sont définies dans `scripts/ceo_automations.py`. Chaque commande est une fonction Python qui peut être appelée via `python scripts/ceo_automations.py <nom_commande>`.

## Comment Ajouter une Nouvelle Commande

### 1. Définir la fonction

Dans `scripts/ceo_automations.py`, ajoutez une nouvelle fonction:

```python
def nouvelle_commande():
    """Description de ce que fait la commande"""
    # Votre code ici
    print("Résultat de la commande")
```

### 2. Ajouter le mapping

Dans la section `if __name__ == "__main__"`, ajoutez la logique pour gérer votre nouvelle commande:

```python
if command == "ma_commande":
    nouvelle_commande()
```

### 3. Mettre à jour l'aide

Modifiez le message d'aide au début du script:

```python
print("\nCommandes disponibles:")
print("  emails    - Résume les emails récents")
print("  priorites - Affiche les priorités actuelles")
print("  checkin   - Crée le weekly check-in template")
print("  ma_commande - Description de votre commande")
```

### 4. Mettre à jour COMMANDES.md

Ajoutez votre nouvelle commande dans `COMMANDES.md`:

```markdown
## 🎯 Ma Nouvelle Commande
```bash
cd scripts && python ceo_automations.py ma_commande
```
Description de ce que fait la commande
```

## Exemples de Commandes Utiles

### Exemple 1: Rapport de tâches du jour

```python
def show_daily_tasks():
    """Affiche les tâches à faire aujourd'hui"""
    try:
        with open('../tasks.md', 'r') as f:
            print("\n📝 TÂCHES DU JOUR")
            print("="*60)
            print(f.read())
    except FileNotFoundError:
        print("\n❌ Fichier tasks.md non trouvé")
```

### Exemple 2: Statistiques rapides

```python
def show_stats():
    """Affiche des statistiques clés"""
    print("\n📊 STATISTIQUES")
    print("="*60)
    print("KPI 1: XXX")
    print("KPI 2: XXX")
```

### Exemple 3: Création rapide de note

```python
def quick_note(note_title):
    """Crée une note rapide"""
    filename = f"notes/{note_title.replace(' ', '_')}.md"
    with open(filename, 'w') as f:
        f.write(f"# {note_title}\n\n")
        f.write(f"Créé le: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        f.write("---\n\n")
    print(f"\n✅ Note créée: {filename}")
```

## Commandes avec Arguments

Pour les commandes qui acceptent des arguments:

```python
if len(sys.argv) > 2:
    argument = sys.argv[2]
else:
    print("Usage: python ceo_automations.py ma_commande <argument>")
    sys.exit(1)
```

## Bonnes Pratiques

1. **Documentation**: Toujours ajouter un docstring à chaque fonction
2. **Gestion d'erreurs**: Utilisez try/except pour gérer les fichiers manquants ou erreurs API
3. **Messages clairs**: Utilisez des emojis et des messages en français cohérents
4. **Séparation**: Pour les scripts complexes, créez des fichiers séparés (comme `gmail_auth.py`, `summarize_emails.py`)

## Structure de Dossiers Recommandée

```
ceo/
├── scripts/
│   ├── ceo_automations.py      # Point d'entrée principal
│   ├── gmail_auth.py            # Authentification Gmail
│   ├── summarize_emails.py      # Logique emails
│   └── requirements.txt         # Dépendances Python
├── automatisations/
│   ├── README.md                # Documentation automatisations
│   └── gmail_setup.md           # Setup Gmail API
├── templates/                   # Templates réutilisables
├── rapports/                    # Rapports générés
├── COMMANDES.md                 # Liste des commandes pour opencode
└── priorites.md                 # Données priorités
```

## Intégration avec Opencode

Une fois votre commande créée, vous pouvez l'utiliser directement via opencode:

1. La commande est listée dans `COMMANDES.md`
2. Je peux l'exécuter avec: `cd scripts && python ceo_automations.py votre_commande`
3. Les utilisateurs peuvent demander: "exécute la commande X" ou "lance X"

## Tests Avant Déploiement

Testez toujours votre commande avant de la considérer comme prête:

```bash
cd scripts
python ceo_automations.py votre_commande
```

Vérifiez que:
- Les fichiers sont lus/écrits correctement
- Les messages d'erreur sont clairs
- La sortie est lisible et utile
