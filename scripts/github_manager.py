"""
Gestionnaire de projets GitHub pour PETITJEAN & WEMEDIA
Permet de créer, gérer et rapporter les issues GitHub
"""

import os
import sys
import json
import argparse
from datetime import datetime
from github import Github, GithubException

# Configuration
ORGANIZATION = "ddpetit"
REPOSITORIES = {
    "PETITJEAN": ["bricov4"],
    "WEMEDIA": ["supernestor", "comparat", "comparem", "zagrow", "my_zagrow"]
}
PRIORITIES = ["Urgent", "Normal", "Low"]
STATUSES = ["Todo", "In Progress", "Review", "Done"]
ENTITIES = ["WEMEDIA", "PETITJEAN"]


class GitHubManager:
    def __init__(self, token=None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN non trouvé. Exportez-le ou passez-le en argument.")
        self.gh = Github(self.token)

    def get_repository(self, repo_name):
        """Récupère un dépôt"""
        return self.gh.get_repo(f"{ORGANIZATION}/{repo_name}")

    def create_issue(self, repo_name, initials, title, description="", 
                    priority="Normal", entity=None, project=None, assignee=None):
        """Crée une issue avec la convention [INITIALES]"""
        repo = self.get_repository(repo_name)
        
        # Convention de nommage
        formatted_title = f"[{initials.upper()}] {title}"
        
        # Body de l'issue
        body = f"""
## Description
{description}

## Métadonnées
- **Entité**: {entity or 'Non spécifié'}
- **Projet**: {project or repo_name}
- **Priorité**: {priority}
- **Créé le**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---
*Créé automatiquement via ceo-management*
"""
        
        # Labels
        labels = [priority]
        if entity:
            labels.append(entity)
        
        try:
            issue = repo.create_issue(
                title=formatted_title,
                body=body,
                labels=labels,
                assignee=assignee
            )
            print(f"✅ Issue créée: {issue.html_url}")
            return issue
        except GithubException as e:
            print(f"❌ Erreur création issue: {e}")
            return None

    def list_issues(self, repo_name=None, initials=None, status="open", entity=None):
        """Liste les issues avec filtres"""
        issues_found = []
        
        repos_to_search = [repo_name] if repo_name else [r for group in REPOSITORIES.values() for r in group]
        
        for repo_name in repos_to_search:
            try:
                repo = self.get_repository(repo_name)
                issues = repo.get_issues(state=status)
                
                for issue in issues:
                    # Filtrer par initiales si demandé
                    if initials:
                        if not issue.title.startswith(f"[{initials.upper()}]"):
                            continue
                    
                    # Filtrer par entité si demandé
                    if entity:
                        has_entity_label = any(entity in str(label) for label in issue.labels)
                        if not has_entity_label:
                            continue
                    
                    issues_found.append({
                        'repo': repo_name,
                        'number': issue.number,
                        'title': issue.title,
                        'url': issue.html_url,
                        'state': issue.state,
                        'labels': [str(label) for label in issue.labels],
                        'created_at': issue.created_at.strftime('%Y-%m-%d'),
                        'assignee': issue.assignee.login if issue.assignee else None
                    })
            except GithubException as e:
                print(f"⚠️ Erreur sur {repo_name}: {e}")
        
        return issues_found

    def update_issue(self, repo_name, issue_number, new_title=None, 
                    new_state=None, add_labels=None, remove_labels=None, comment=None):
        """Met à jour une issue"""
        repo = self.get_repository(repo_name)
        issue = repo.get_issue(issue_number)
        
        if new_title:
            issue.edit(title=new_title)
        
        if new_state == "close":
            issue.edit(state="closed")
        elif new_state == "open":
            issue.edit(state="open")
        
        if add_labels:
            for label in add_labels:
                issue.add_to_labels(label)
        
        if comment:
            issue.create_comment(comment)
        
        print(f"✅ Issue {issue_number} mise à jour")

    def close_issue(self, repo_name, issue_number, comment=None):
        """Ferme une issue"""
        repo = self.get_repository(repo_name)
        issue = repo.get_issue(issue_number)
        
        if comment:
            issue.create_comment(comment)
        
        issue.edit(state="closed")
        print(f"✅ Issue {issue_number} fermée")

    def generate_report(self, output_file="rapport_projets.md"):
        """Génère un rapport de toutes les issues"""
        all_issues = self.list_issues(status="open")
        
        # Grouper par entité et projet
        grouped = {}
        for issue in all_issues:
            entity = next((label for label in issue['labels'] if label in ENTITIES), "Autre")
            if entity not in grouped:
                grouped[entity] = {}
            if issue['repo'] not in grouped[entity]:
                grouped[entity][issue['repo']] = []
            grouped[entity][issue['repo']].append(issue)
        
        # Générer le rapport
        report = f"# Rapport Projets PETITJEAN & WEMEDIA\n\n"
        report += f"**Généré le**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        report += f"**Total issues ouvertes**: {len(all_issues)}\n\n"
        
        for entity, repos in grouped.items():
            report += f"## 📦 {entity}\n\n"
            for repo, issues in repos.items():
                report += f"### {repo}\n\n"
                for issue in issues:
                    report += f"- **{issue['title']}**\n"
                    report += f"  - URL: {issue['url']}\n"
                    report += f"  - Labels: {', '.join(issue['labels'])}\n"
                    report += f"  - Créé: {issue['created_at']}\n\n"
        
        # Sauvegarder le rapport
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Rapport généré: {output_file}")

    def import_tasks_from_file(self, input_file, repo_name, default_entity=None):
        """Importe des tâches depuis un fichier JSON ou CSV"""
        if input_file.endswith('.json'):
            with open(input_file, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
        elif input_file.endswith('.csv'):
            import csv
            tasks = []
            with open(input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                tasks = list(reader)
        else:
            print("❌ Format non supporté (JSON ou CSV uniquement)")
            return
        
        for task in tasks:
            self.create_issue(
                repo_name=repo_name,
                initials=task.get('initials', 'XX'),
                title=task.get('title', 'Sans titre'),
                description=task.get('description', ''),
                priority=task.get('priority', 'Normal'),
                entity=default_entity,
                project=repo_name
            )
        
        print(f"✅ {len(tasks)} tâches importées")


def main():
    parser = argparse.ArgumentParser(description='GitHub Manager pour PETITJEAN & WEMEDIA')
    
    # Créer une issue
    parser.add_argument('--create', action='store_true', help='Créer une nouvelle issue')
    parser.add_argument('--repo', help='Nom du dépôt')
    parser.add_argument('--initials', help='Initiales de l\'employé')
    parser.add_argument('--title', help='Titre de l\'issue')
    parser.add_argument('--description', help='Description de l\'issue', default='')
    parser.add_argument('--priority', choices=PRIORITIES, default='Normal')
    parser.add_argument('--entity', choices=ENTITIES, help='Entité (WEMEDIA ou PETITJEAN)')
    
    # Lister les issues
    parser.add_argument('--list', action='store_true', help='Lister les issues')
    parser.add_argument('--filter-initials', help='Filtrer par initiales')
    parser.add_argument('--filter-entity', choices=ENTITIES, help='Filtrer par entité')
    parser.add_argument('--status', choices=['open', 'closed', 'all'], default='open')
    
    # Mettre à jour une issue
    parser.add_argument('--update', type=int, help='Numéro de l\'issue à mettre à jour')
    parser.add_argument('--close', action='store_true', help='Fermer l\'issue')
    parser.add_argument('--add-label', action='append', help='Ajouter un label')
    parser.add_argument('--comment', help='Ajouter un commentaire')
    
    # Rapports
    parser.add_argument('--report', action='store_true', help='Générer un rapport')
    parser.add_argument('--output', help='Fichier de sortie du rapport', default='rapport_projets.md')
    
    # Import
    parser.add_argument('--import', dest='import_file', help='Importer des tâches depuis un fichier')
    
    # Token
    parser.add_argument('--token', help='GitHub Token (sinon utilise GITHUB_TOKEN)')
    
    args = parser.parse_args()
    
    # Initialiser le manager
    try:
        manager = GitHubManager(token=args.token)
    except ValueError as e:
        print(e)
        sys.exit(1)
    
    # Exécuter les commandes
    if args.create:
        if not args.repo or not args.initials or not args.title:
            print("❌ --repo, --initials et --title sont requis pour créer une issue")
            sys.exit(1)
        
        manager.create_issue(
            repo_name=args.repo,
            initials=args.initials,
            title=args.title,
            description=args.description,
            priority=args.priority,
            entity=args.entity
        )
    
    elif args.list:
        issues = manager.list_issues(
            repo_name=args.repo,
            initials=args.filter_initials,
            status=args.status,
            entity=args.filter_entity
        )
        
        print(f"\n📋 {len(issues)} issue(s) trouvée(s):\n")
        for issue in issues:
            print(f"[{issue['repo']}] #{issue['number']}: {issue['title']}")
            print(f"  URL: {issue['url']}")
            print(f"  Labels: {', '.join(issue['labels'])}")
            print()
    
    elif args.update or args.close:
        if not args.repo:
            print("❌ --repo est requis pour mettre à jour une issue")
            sys.exit(1)
        
        if args.close:
            manager.close_issue(args.repo, args.update, comment=args.comment)
        else:
            manager.update_issue(
                repo_name=args.repo,
                issue_number=args.update,
                add_labels=args.add_label,
                comment=args.comment
            )
    
    elif args.report:
        manager.generate_report(output_file=args.output)
    
    elif args.import_file:
        if not args.repo:
            print("❌ --repo est requis pour importer des tâches")
            sys.exit(1)
        manager.import_tasks_from_file(args.import_file, args.repo, args.entity)


if __name__ == "__main__":
    main()