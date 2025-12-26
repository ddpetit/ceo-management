#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

DAILY_CHECKIN_DIR = Path(__file__).parent.parent / 'logs' / 'daily_checkins'
STATS_FILE = Path(__file__).parent.parent / 'logs' / 'email_stats.json'

def get_today_log():
    today_key = datetime.now().strftime('%Y-%m-%d')
    log_file = DAILY_CHECKIN_DIR / f"{today_key}.json"
    
    if not log_file.exists():
        print(f"❌ Aucun checkin trouvé pour aujourd'hui ({today_key})")
        return None
    
    with open(log_file, 'r') as f:
        return json.load(f)

def save_today_log(data):
    today_key = datetime.now().strftime('%Y-%m-%d')
    log_file = DAILY_CHECKIN_DIR / f"{today_key}.json"
    
    with open(log_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def show_status():
    data = get_today_log()
    if not data:
        return
    
    tasks = data.get('tasks', [])
    todo = [t for t in tasks if t['status'] == 'TODO']
    in_progress = [t for t in tasks if t['status'] == 'IN_PROGRESS']
    done = [t for t in tasks if t['status'] == 'DONE']
    
    print("\n" + "="*70)
    print(f"📊 STATUS DU JOUR - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("="*70)
    
    print(f"\n🔵 À FAIRE ({len(todo)}):")
    for t in todo:
        print(f"   [{t['priority']}] {t['task']}")
    
    print(f"\n🟡 EN COURS ({len(in_progress)}):")
    for t in in_progress:
        print(f"   [{t['priority']}] {t['task']}")
    
    print(f"\n✅ TERMINÉ ({len(done)}):")
    for t in done:
        print(f"   {t['task']}")
    
    print("\n" + "="*70 + "\n")

def update_task_status():
    data = get_today_log()
    if not data:
        return
    
    tasks = data.get('tasks', [])
    
    print("\nTâches actuelles:")
    for i, t in enumerate(tasks, 1):
        status_emoji = {'TODO': '⏳', 'IN_PROGRESS': '🔄', 'DONE': '✅'}
        print(f"{i}. {status_emoji[t['status']]} {t['task']} ({t['priority']})")
    
    while True:
        choice = input("\nNuméro de tâche à mettre à jour (ou 'fin'): ").strip()
        if choice.lower() in ['fin', '']:
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tasks):
                current = tasks[idx]['status']
                options = ['TODO', 'IN_PROGRESS', 'DONE']
                current_idx = options.index(current)
                new_idx = (current_idx + 1) % 3
                tasks[idx]['status'] = options[new_idx]
                
                print(f"✅ {tasks[idx]['task']} → {tasks[idx]['status']}")
            else:
                print("❌ Numéro invalide")
        except ValueError:
            print("❌ Entrée invalide")
    
    data['tasks'] = tasks
    save_today_log(data)
    print("\n💾 Sauvegardé!")

def add_task():
    data = get_today_log()
    if not data:
        return
    
    task = input("Nouvelle tâche: ").strip()
    priority = input("Priorité (H/M/B)? [M] ").strip().upper() or 'M'
    priority_map = {'H': 'HIGH', 'M': 'MEDIUM', 'B': 'LOW'}
    priority = priority_map.get(priority, 'MEDIUM')
    
    data['tasks'].append({
        'task': task,
        'priority': priority,
        'status': 'TODO'
    })
    
    save_today_log(data)
    print(f"✅ Tâche ajoutée: {task}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'status':
            show_status()
        elif command == 'update':
            update_task_status()
        elif command == 'add':
            add_task()
        else:
            print("Commandes disponibles: status, update, add")
    else:
        show_status()
