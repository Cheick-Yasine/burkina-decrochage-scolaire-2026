# Cartographie et anticipation du risque de décrochage scolaire au Burkina Faso

**Data Challenge Burkina — Édition Éducation 2026 — Défi 1**

> Où le risque de décrochage est-il le plus fort, par région et province, et comment l'anticiper ?

## Vision du projet

Construire une plateforme web d'aide à la décision et de vigilance scolaire couvrant trois cycles :
- **Primaire** : maintien, abandon, redoublement et achèvement ;
- **Post-primaire** : transition CM2–6e, maintien et abandon ;
- **Secondaire** : maintien, abandon et vulnérabilités du parcours.

La couverture des trois cycles constitue l'ambition fonctionnelle. Elle sera réalisée progressivement, en commençant par le primaire, puis en intégrant le post-primaire et le secondaire selon la disponibilité et la comparabilité des sources.

La plateforme visée réunira :
1. un tableau de bord cartographique multicouche, à l'échelle géographique réellement disponible ;
2. un **Score de Risque de Décrochage (SRD)** documenté et interprétable ;
3. lorsque les données cibles et historiques le permettent, un modèle prédictif évalué hors échantillon ;
4. des recommandations opérationnelles pour les décideurs et acteurs de terrain.

## Périmètre du challenge et ambition élargie

Le Défi 1 du Data Challenge demande d'identifier où le risque est le plus fort par région et comment l'anticiper. Les données cœur annoncées sont :
- tableaux de bord du primaire : abandon, redoublement et achèvement (2015–2024) ;
- annuaires du primaire : abandons par province ;
- tableaux de bord du post-primaire : transition.

Les données d'appui facultatives citées comprennent les rapports ESU sur les écoles fermées, les données de personnes déplacées internes, l'EHCVM 2021 et les profils de pauvreté, ainsi que l'EDS 2021 sur le mariage précoce des filles.

**Le secondaire fait partie de la vision de la plateforme, mais n'est pas explicitement listé parmi les données cœur du Défi 1 dans la présentation de l'organisateur.** Il sera intégré après identification de sources officielles adéquates. Nous ne supposerons pas que ces données sont déjà présentes.

## Sources déjà inventoriées

Le classeur DGESS *Données statistiques préscolaire et primaire 2016–2025* comprend 14 feuilles : préscolaire, effectifs du primaire, nouveaux entrants au CP1, TBA, TBS, achèvement, réussite au CEP, indices de parité et nombre d'écoles.

L'inventaire effectué ne fait pas apparaître de tableau explicite des abandons par province dans ce classeur. Les effectifs, TBS, TAP et résultats au CEP sont des indicateurs de contexte ; ils ne doivent pas être présentés comme des abandons observés.

Les données brutes restent locales et ne sont pas versionnées dans ce dépôt public.

## Architecture fonctionnelle

- **Collecte** : sources, provenance, période, géographie, droits d'usage.
- **Nettoyage** : contrôles, harmonisation des libellés et journal des corrections.
- **Transformation** : indicateurs comparables par cycle, année et territoire.
- **Analyse** : tendances, transitions, disparités et analyse spatiale.
- **Modélisation** : indice SRD d'abord ; modèle prédictif seulement si une cible fiable et assez d'historique sont disponibles.
- **Application** : carte, filtres par cycle, fiches territoriales, niveaux d'alerte et recommandations.
- **Interprétation** : limites, décisions possibles et suivi des actions.

Voir [l'architecture cible](documentation/architecture_cible.md) et le [plan de travail](documentation/plan_travail.md).

## Principes méthodologiques non négociables

- Distinguer **abandon observé**, **signal indirect de vulnérabilité** et **risque estimé**.
- Une baisse d'effectifs ne prouve pas un abandon : migrations, déplacements, redoublement, changements de périmètre et fermetures peuvent aussi l'expliquer.
- Ne pas confondre année scolaire et année civile.
- Ne pas mélanger les anciennes régions (13) et les nouvelles (17) sans table de correspondance validée.
- Harmoniser les provinces et privilégier les P-codes lorsqu'ils sont disponibles.
- Retirer les lignes de total des calculs analytiques, tout en les conservant éventuellement pour les contrôles de cohérence.
- Vérifier les agrégats avec les publications d'origine.
- Documenter producteur, publication, année, page/tableau et transformation.
- Construire un indice transparent avant tout algorithme complexe.
- Ne pas annoncer une probabilité prédictive sans cible observée, protocole de validation temporelle et mesure de performance.
- Les données brutes doivent être nettoyées localement avant tout recours à une IA ; ne jamais téléverser les données brutes ou sensibles.

## Organisation du dépôt

- `data/raw/` : données sources locales, non versionnées.
- `data/processed/` : données préparées, partageables uniquement si autorisées.
- `data/final/` : agrégats finaux autorisés.
- `01_collecte/` à `05_interpretation/` : cinq étapes du challenge.
- `04_analyse/` : analyses séparées par cycle.
- `06_modelisation/` : indice SRD, prédiction et évaluation.
- `07_application/` : application cartographique et tableau de bord.
- `documentation/` : dictionnaire, méthode, architecture et rapport.
- `tests/` : contrôles automatisés.

Les fichiers de données brutes ne doivent jamais être ajoutés au dépôt public. Les données préparées ne sont publiées qu'après vérification des conditions de diffusion.

## Validation temporelle

Le conseil de l'organisateur est d'entraîner sur 2017–2023 et de tester sur 2024–2025, si les observations sont suffisantes et comparables. Ce découpage sera adapté au cycle, à la cible disponible et à la période réelle des sources ; il ne sera pas appliqué mécaniquement.

## Livrables

- données de travail et journaux de nettoyage documentés ;
- dictionnaire et schéma harmonisé ;
- indicateurs par cycle et territoire ;
- indice SRD interprétable ;
- évaluation du modèle prédictif, si réalisable ;
- carte/tableau de bord relançable ;
- recommandations et documentation de 15 pages maximum pour le challenge.

## État d'avancement

- [x] Dépôt GitHub initialisé.
- [x] Inventaire structurel du classeur DGESS (14 feuilles).
- [x] Première cartographie des tableaux de la feuille PRESCOLAIRE.
- [x] Dictionnaire initial et rapports de diagnostic locaux.
- [ ] Vérification complète des libellés, unités et périodes.
- [ ] Acquisition des abandons par province et données de transition post-primaire.
- [ ] Identification de sources officielles pour le secondaire.
- [ ] Harmonisation géographique et nettoyage des données autorisées.
- [ ] Calcul des indicateurs et contrôles.
- [ ] Construction et évaluation du SRD.
- [ ] Carte, tableau de bord et recommandations.
- [ ] Documentation finale et démonstration.

## Références du challenge

Data Challenge Burkina, Édition Éducation 2026 : *Le document du challenge* et *Rencontre en ligne avec les équipes*, 15 novembre 2026.