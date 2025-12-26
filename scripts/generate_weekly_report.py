#!/usr/bin/env python3
import os
from datetime import datetime
import json

# Configuration des priorités
priorites_file = "priorites.md"
projects_dir = "projets"

def get_week_number():
    return datetime.now().isocalendar()[1]

def create_weekly_report():
    week = get_week_number()
    report_file = f"rapports/semaine_{week}.md"
    
    if os.path.exists(priorites_file):
        with open(priorites_file, 'r') as f:
            content = f.read()
            print("Contenu des priorités actuel :")
            print(content)

if __name__ == "__main__":
    create_weekly_report()
