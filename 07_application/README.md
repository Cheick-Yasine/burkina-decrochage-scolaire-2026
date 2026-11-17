# Application web — Vigie École

**Vigie École** est l'interface analytique du projet : une plateforme de vigilance scolaire qui transforme les indicateurs validés en lectures territoriales lisibles.

## Lancer l'application

Depuis la racine du dépôt :

```powershell
python -m pip install -r requirements.txt
python -m streamlit run .\07_application\vigie_ecole.py
```

Le fichier traité attendu est :

`data/processed/indicateurs_primaire.csv`

Les données brutes ne doivent jamais être ajoutées au dépôt public.

## Écrans disponibles

- **Vue d'ensemble** : repères descriptifs, trajectoire et comparaison territoriale.
- **Explorer les territoires** : classement pour une période et un indicateur choisis.
- **Suivre les évolutions** : courbes par région.
- **Qualité & méthode** : contrôles automatiques et limites d'interprétation.

## Règles de présentation

- Aucun chiffre fictif ou indicateur simulé.
- Les indicateurs descriptifs ne sont jamais renommés « abandons » ou « risque de décrochage ».
- Les clés territoriales répétées bloquent les classements afin d'éviter une conclusion trompeuse.
- Les années scolaires et civiles restent distinguées.
- La carte géographique ne sera activée qu'après intégration de limites administratives vérifiées et compatibles avec le découpage historique des données.

## Prochaines évolutions

1. Corriger et valider les données sources.
2. Ajouter une carte des 13 anciennes régions, avec avertissement sur le découpage.
3. Intégrer les abandons par province et la transition post-primaire dès que les sources officielles sont disponibles.
4. Construire un Score de Risque de Décrochage documenté, puis évaluer un modèle uniquement si une cible fiable existe.
