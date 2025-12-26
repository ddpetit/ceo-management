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

## 🎯 Workflow quotidien

**Matin**
1. `python ceo_automations.py emails` - Voir les emails importants
2. `python ceo_automations.py priorites` - Revoir les priorités
3. Mettre à jour `priorites.md`

**Lundi**
- `python ceo_automations.py checkin` - Démarrer le weekly check-in
- Remplir `rapports/semaine_X.md`

**Vendredi**
- Finaliser le weekly check-in
- Planifier la semaine suivante

## ⚡ Rapide

Je peux exécuter ces commandes pour vous. Dites-moi simplement :
- "résumé emails" pour voir les emails
- "voir priorités" pour afficher vos priorités
- "checkin" pour créer un rapport hebdomadaire
