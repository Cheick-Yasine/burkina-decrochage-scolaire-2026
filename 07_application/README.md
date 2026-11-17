# Application web — Vigie École

**Vigie École** reprend le système visuel de HAKIMO : police Manrope, palette bleu / bleu nuit, navigation latérale sombre, cartes blanches, filtres et graphiques interactifs. L'application est construite avec **FastAPI + HTML/CSS/JavaScript** (pas Streamlit).

## Lancer l'application en local

Depuis la racine du dépôt :

```powershell
python -m pip install -r requirements.txt
python -m uvicorn 07_application.main:app --reload
```

Le nom du dossier commençant par un chiffre rend l'import Python direct invalide. Utilise plutôt cette commande depuis la racine :

```powershell
python -m uvicorn main:app --app-dir .\07_application --reload
```

Ouvre ensuite : http://127.0.0.1:8000

## Données attendues

`data/processed/indicateurs_primaire.csv`

Les données brutes ne doivent jamais être ajoutées au dépôt public.

## Écrans

- **Vue d'ensemble** : indicateurs descriptifs, trajectoire et comparaison.
- **Explorer les territoires** : classement régional pour une période.
- **Évolutions scolaires** : comparaison des trajectoires par région.
- **Qualité & méthode** : contrôles et limites d'interprétation.

## Principes

- Aucun chiffre fictif.
- Les indicateurs descriptifs ne sont jamais présentés comme des abandons ou un score de risque.
- Les doublons logiques bloquent l'analyse pour éviter les classements trompeurs.
- Les années scolaires et civiles restent distinguées.
- La carte ne sera intégrée qu'avec des limites administratives vérifiées et compatibles avec le découpage historique.
- Le score de risque et le modèle prédictif viendront après l'intégration des données d'abandon par province et des autres sources officielles.
