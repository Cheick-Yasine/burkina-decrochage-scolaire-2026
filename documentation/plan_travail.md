# Plan de travail — trois cycles d'enseignement

## Stratégie générale

L'ambition fonctionnelle couvre primaire, post-primaire et secondaire. La réalisation est progressive : produire d'abord un socle primaire vérifiable, intégrer ensuite les données de transition et de maintien du post-primaire, puis étendre au secondaire lorsque des sources officielles comparables sont obtenues.

## Phase A — Remise du challenge (priorité immédiate)

1. Terminer le diagnostic du classeur DGESS primaire/pré-primaire sans modifier le fichier source.
2. Identifier dans le Data Pack les tableaux cœur du Défi 1 : abandon/redoublement/achèvement au primaire, abandons par province, transition post-primaire.
3. Référencer chaque source : producteur, titre, année, page/tableau, niveau géographique, unité et définition.
4. Nettoyer localement les jeux de données retenus ; conserver un journal des corrections.
5. Calculer des indicateurs région/province/année et contrôler les agrégats.
6. Produire une première analyse et une carte/tableau de bord si les données géographiques sont disponibles.
7. Rédiger une documentation concise, 15 pages maximum, et préparer une démonstration relançable.

## Phase B — Extension au post-primaire

1. Obtenir les séries de transition primaire → post-primaire et les indicateurs de maintien/abandon disponibles.
2. Vérifier les définitions et les dénominateurs des taux.
3. Construire les indicateurs propres au cycle.
4. Relier les observations par territoire, période et P-code si disponibles.
5. Comparer les transitions et vulnérabilités sans supposer que les séries sont directement comparables au primaire.

## Phase C — Extension au secondaire

1. Identifier les annuaires et tableaux de bord officiels couvrant le secondaire.
2. Documenter les niveaux (secondaire général/technique si présents), périodes et unités.
3. Nettoyer et harmoniser les territoires et les années.
4. Calculer les indicateurs spécifiques au secondaire.
5. Intégrer le cycle à l'interface après validation de la qualité des données.

## Phase D — Indice SRD et prédiction

1. Définir une fiche méthodologique par composante du SRD.
2. Construire une baseline descriptive puis un indice composite.
3. Faire valider la sensibilité des pondérations et la stabilité temporelle.
4. N'entraîner un modèle prédictif que si une cible d'abandon observé est disponible et assez d'observations comparables existent.
5. Utiliser un découpage temporel conforme au conseil du challenge (2017–2023 entraînement, 2024–2025 test si possible).
6. Publier métriques, limites, erreurs et cas d'usage ; ne pas assimiler le SRD à une probabilité.

## Phase E — Plateforme et recommandations

1. Développer la carte multi-cycles avec filtres.
2. Ajouter des couches contextuelles uniquement après vérification des sources.
3. Présenter pour chaque territoire les faits observés, signaux indirects et estimations séparément.
4. Relier les alertes à des pistes d'action réalistes.
5. Tester la compréhension avec un utilisateur cible et documenter la reproductibilité.

## Jalons et critères de sortie

| Jalon | Critère de validation |
|---|---|
| Sources | Provenance, définition, période et géographie documentées |
| Nettoyage | Règles reproductibles, corrections journalisées, totaux contrôlés |
| Indicateurs | Formules, unités, dénominateurs et limites documentés |
| Comparabilité | Années et découpages territoriaux vérifiés |
| SRD | Composantes transparentes et interprétables |
| Prédiction | Label fiable, validation temporelle et métriques disponibles |
| Application | Résultats traçables jusqu'aux sources |
| Documentation | 15 pages maximum pour le livrable du challenge |

## Règles de décision

- Si une donnée n'existe pas ou n'est pas comparable, marquer « non disponible » plutôt que l'estimer silencieusement.
- Si seul un signal indirect est disponible, le nommer « signal de vulnérabilité ».
- Ne pas retarder la remise du challenge pour développer une extension secondaire sans source validée.
- Prioriser peu de sources bien exploitées plutôt qu'un grand nombre de fichiers superficiellement analysés.
