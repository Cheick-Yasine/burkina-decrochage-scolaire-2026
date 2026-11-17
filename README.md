# Cartographie et anticipation du risque de décrochage scolaire au Burkina Faso

**Data Challenge Burkina — Édition Éducation 2026 — Défi 1**

> Où le risque de décrochage est-il le plus fort, par région, et comment l'anticiper ?

## Objectif

Construire une solution d'aide à la décision qui décrit les disparités territoriales liées au parcours scolaire, repère les zones nécessitant une attention particulière et, si les données le permettent, estime les risques futurs.

La solution visée comprendra :
- une base de données scolaire documentée et harmonisée ;
- des indicateurs calculés et vérifiés ;
- une analyse temporelle et territoriale ;
- une carte ou un tableau de bord d'alerte ;
- un indice de risque transparent, puis éventuellement un modèle prédictif évalué.

**Attention :** un indicateur indirect (baisse des effectifs, faible achèvement, etc.) ne constitue pas à lui seul une mesure du décrochage. Les résultats distingueront clairement les mesures observées, les indicateurs indirects et les estimations.

## Sources de départ

Le classeur fourni pour le challenge est : *Données statistiques préscolaire et primaire 2016-2025* (DGESS, Ministère de l'Éducation nationale). Il contient 14 feuilles :
- PRESCOLAIRE ;
- Feuil1 à Feuil13, comprenant notamment les effectifs du primaire, les nouveaux inscrits au CP1, les TBA, TBS, taux d'achèvement, réussite au CEP, IPS et nombre d'écoles.

Le classeur constitue une base de travail, mais l'inventaire initial ne fait pas apparaître de tableau explicite des abandons par province. Il faudra donc retrouver dans le Data Pack / les annuaires DGESS les tableaux d'abandon par province et les données de transition post-primaire mentionnés pour le Défi 1.

## Parcours de traitement

Le dépôt suit les cinq étapes recommandées par l'organisation :

1. [Collecte](01_collecte/README.md) — sources, provenance et versions.
2. [Nettoyage](02_nettoyage/README.md) — qualité, harmonisation et journal des corrections.
3. [Transformation](03_transformation/README.md) — indicateurs et modèle commun.
4. [Analyse](04_analyse/README.md) — statistiques, tendances et modèles.
5. [Interprétation](05_interpretation/README.md) — carte, tableau de bord et recommandations.

## Organisation du dépôt

- `data/raw/` : données sources locales, non versionnées.
- `data/processed/` : données préparées, à publier uniquement si leur diffusion est autorisée.
- `data/final/` : données agrégées finales autorisées.
- `src/` : code Python de traitement et d'analyse.
- `documentation/` : dictionnaire, méthode et rapport.
- `tests/` : contrôles de qualité.

Les fichiers de données brutes ne doivent pas être ajoutés à un dépôt public. Le document de présentation du challenge précise que les données sont réservées à l'usage du concours et demande de ne pas envoyer les données brutes à une IA. Le travail de préparation doit donc être réalisé localement ; seuls des résultats et fichiers dont la publication est autorisée seront partagés.

## Démarrage

Python 3.10 ou supérieur recommandé.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
pip install -r requirements.txt
```

Les scripts seront ajoutés au fur et à mesure que le dictionnaire réel des colonnes et les règles de nettoyage auront été vérifiés.

## Principes méthodologiques

- Conserver l'année scolaire (ex. 2024-2025) et ne pas la confondre avec l'année civile.
- Retirer les lignes de total avant les calculs.
- Harmoniser les noms de régions et de provinces sans fusion géographique arbitraire.
- Tenir compte du passage de 13 anciennes régions à 17 nouvelles régions.
- Utiliser les P-codes comme clés de rapprochement lorsque disponibles.
- Vérifier les totaux calculés avec les publications d'origine.
- Citer chaque source : producteur, publication et année.
- Si un modèle est construit, suivre le conseil du challenge : entraînement 2017-2023 et test 2024-2025, sous réserve que les observations soient suffisantes et comparables.

## Livrables attendus

- Données brutes référencées, données propres et journal de nettoyage.
- Schéma de données et dictionnaire des variables.
- Indicateurs, graphiques, carte ou tableau de bord.
- Code du modèle et mesure de sa fiabilité si une prévision est réalisable.
- Documentation de 15 pages maximum expliquant la réponse au défi.

## État du projet

- [x] Dépôt initialisé.
- [x] Arborescence documentaire créée.
- [ ] Inventaire détaillé des colonnes et des unités.
- [ ] Acquisition des tableaux d'abandon par province.
- [ ] Harmonisation géographique et nettoyage.
- [ ] Calcul des indicateurs et contrôles.
- [ ] Analyse et carte d'alerte.
- [ ] Évaluation éventuelle d'un modèle prédictif.
- [ ] Rapport final et démonstration.

## Référence

Data Challenge Burkina, Édition Éducation 2026 : *Le document du challenge* et *Rencontre en ligne avec les équipes*, 15 novembre 2026. Source statistique principale annoncée : DGESS, Ministère de l'Éducation nationale.
