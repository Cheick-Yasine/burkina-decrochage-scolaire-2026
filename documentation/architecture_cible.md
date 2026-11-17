# Architecture cible — plateforme de vigilance scolaire

## 1. Finalité

La plateforme doit aider à repérer les territoires et les cycles où les parcours scolaires présentent des signaux de fragilité, puis à orienter les investigations et les actions. Elle couvre à terme le primaire, le post-primaire et le secondaire.

## 2. Périmètre des données : ce qui est confirmé et ce qui reste à acquérir

### Données cœur confirmées par le cadrage du Défi 1
- Primaire : tableaux de bord d'abandon, redoublement et achèvement (2015–2024).
- Primaire : annuaires avec abandons par province.
- Post-primaire : tableaux de bord de transition.

### Données d'appui proposées par l'organisateur
- Rapports ESU sur les écoles fermées.
- Personnes déplacées internes (PDI).
- EHCVM 2021 et profils de pauvreté.
- EDS 2021 sur le mariage précoce des filles.

### Extension secondaire
La note d'intention de l'équipe inclut le secondaire. Les sources officielles correspondantes, leur granularité géographique, leur période et leurs définitions doivent être identifiées avant tout indicateur ou modèle. Ne pas extrapoler les données du primaire au secondaire.

### Classeur DGESS actuellement inventorié
Le classeur 2016–2025 contient des effectifs et indicateurs du préscolaire/primaire (dont TBA, TBS, TAP, CEP, IPS et nombre d'écoles). L'inventaire ne montre pas de tableau explicite d'abandon par province. Ces variables sont des facteurs contextuels ou des signaux indirects, pas des labels d'abandon.

## 3. Modèle conceptuel commun

Chaque observation analytique devra, si les sources le permettent, être décrite par :
- cycle : primaire, post-primaire ou secondaire ;
- année scolaire (conservée sous forme explicite) ;
- territoire : région, province et P-code lorsqu'ils existent ;
- indicateur, valeur, unité et sexe/stratification éventuelle ;
- source, publication, page/tableau et date d'extraction ;
- statut de mesure : observé, calculé ou estimé ;
- niveau de qualité / comparabilité.

Les niveaux géographiques et les années ne seront harmonisés que si une correspondance documentée existe.

## 4. Chaîne de traitement

1. Collecter et référencer les sources.
2. Nettoyer localement : types, valeurs manquantes, doublons, unités, libellés, géographie.
3. Transformer en tables longues harmonisées par cycle, période et territoire.
4. Calculer les indicateurs et vérifier les agrégats avec les publications.
5. Analyser tendances, disparités et transitions.
6. Construire un indice SRD transparent.
7. Entraîner un modèle prédictif uniquement si une cible observée et des séries suffisantes existent.
8. Publier une interface cartographique avec filtres et explications.

## 5. Score de Risque de Décrochage (SRD)

Le SRD sera d'abord un indice composite interprétable, pas une probabilité. Chaque composante devra avoir une définition, une source, une direction attendue, une règle de normalisation et une pondération justifiée.

Composantes candidates à évaluer selon la disponibilité :
- abandon observé ;
- redoublement ;
- achèvement et transition entre cycles ;
- évolution des effectifs (signal indirect seulement) ;
- fermeture d'écoles / perturbation sécuritaire ;
- déplacement de population ;
- pauvreté et facteurs socio-économiques ;
- accessibilité de l'offre scolaire.

Ne pas intégrer une composante simplement parce qu'elle est mentionnée dans la note d'intention : il faut une source, une couverture temporelle et une granularité compatibles.

### Étiquettes de sortie à distinguer
- **Abandon observé** : indicateur officiel fourni par la source.
- **Vulnérabilité** : indice calculé à partir de facteurs documentés.
- **Risque prédit** : sortie d'un modèle supervisé évalué sur des années non utilisées à l'entraînement.

## 6. Modèle prédictif et validation

Le conseil du challenge est un entraînement 2017–2023 et un test 2024–2025, sous réserve de données suffisantes. La validation doit être temporelle et conduite séparément par cycle lorsque les données le permettent.

Mesurer au minimum les performances adaptées à la cible, comparer à une baseline simple et documenter les limites. Sans label fiable d'abandon, ne pas entraîner un classifieur qui prétend prédire l'abandon.

## 7. Interface cible

- Carte à l'échelle géographique la plus fine réellement disponible.
- Filtres : cycle, année scolaire, région/province, sexe et indicateur.
- Couches contextuelles activables avec source et date.
- Fiche territoire : observations, tendances, SRD, qualité et limites.
- Alertes explicables et recommandations reliées aux facteurs observés.
- Aucune zone ne doit être qualifiée de « décrochage élevé » sur la seule base d'une baisse d'effectifs.

## 8. Gouvernance et sécurité

Les données brutes restent locales et ne sont pas poussées sur GitHub. Les données préparées ne sont publiées que si les règles de diffusion le permettent. Le nettoyage se fait avant tout recours à une IA. Chaque source et chaque correction sont documentées.
