
from pathlib import Path
from collections import Counter
import json
import re
import openpyxl

# Chemins du projet
PROJET = Path(__file__).resolve().parents[2]

FICHIER_SOURCE = (
    PROJET
    / "data"
    / "raw"
    / "DONNEES_STATISTIQUES_PRESCOLAIRE_PRIMAIRE_2016_2025.xlsx"
)

DOSSIER_RAPPORTS = PROJET / "documentation" / "rapports"
DOSSIER_RAPPORTS.mkdir(parents=True, exist_ok=True)

FICHIER_RAPPORT = DOSSIER_RAPPORTS / "controle_qualite_structure.txt"
FICHIER_JSON = DOSSIER_RAPPORTS / "controle_qualite_structure.json"


def texte_cellule(valeur):
    """Retourne uniquement les libellés textuels."""
    if isinstance(valeur, str):
        return valeur.strip()
    return ""


def est_total(libelle):
    texte = libelle.upper()
    mots = ["TOTAL", "ENSEMBLE", "TOUTES LES REGIONS"]
    return any(mot in texte for mot in mots)


def extraire_annees(valeurs):
    annees = set()
    for valeur in valeurs:
        if isinstance(valeur, str):
            correspondances = re.findall(
                r"20\d{2}\s*[-/]\s*20\d{2}", valeur
            )
            annees.update(correspondances)
    return sorted(annees)


def analyser_feuille(feuille):
    lignes_non_vides = 0
    cellules_vides = 0
    cellules_numeriques = 0
    cellules_formules = 0
    libelles = []
    annees = set()
    lignes_total = 0
    textes_entete = []

    for ligne in feuille.iter_rows():
        valeurs_ligne = [cellule.value for cellule in ligne]

        if any(valeur is not None for valeur in valeurs_ligne):
            lignes_non_vides += 1

        for cellule in ligne:
            valeur = cellule.value

            if valeur is None:
                cellules_vides += 1
            elif isinstance(valeur, str) and valeur.startswith("="):
                cellules_formules += 1
            elif isinstance(valeur, (int, float)):
                cellules_numeriques += 1

            texte = texte_cellule(valeur)

            if texte:
                if len(textes_entete) < 100:
                    textes_entete.append(texte)

                annees.update(extraire_annees([texte]))

        # Les trois premières colonnes servent à repérer
        # les libellés, sans extraire les valeurs statistiques.
        for valeur in valeurs_ligne[:3]:
            texte = texte_cellule(valeur)
            if texte:
                libelles.append(texte)

        if any(est_total(texte_cellule(v)) for v in valeurs_ligne[:3]):
            lignes_total += 1

    compte_libelles = Counter(libelles)
    doublons = [
        {"libelle": libelle, "occurrences": nombre}
        for libelle, nombre in compte_libelles.items()
        if nombre > 1
    ]

    return {
        "nom_feuille": feuille.title,
        "dimensions": {
            "lignes_max": feuille.max_row,
            "colonnes_max": feuille.max_column,
        },
        "lignes_non_vides": lignes_non_vides,
        "cellules_vides": cellules_vides,
        "cellules_numeriques": cellules_numeriques,
        "cellules_formules": cellules_formules,
        "nombre_lignes_total_detectees": lignes_total,
        "annees_detectees": sorted(annees),
        "plages_fusionnees": [
            str(plage) for plage in feuille.merged_cells.ranges
        ],
        "libelles_reperes": sorted(set(libelles), key=str.casefold),
        "libelles_repetes": doublons,
        "aperçu_entetes_textuels": textes_entete[:30],
    }


def main():
    if not FICHIER_SOURCE.exists():
        raise FileNotFoundError(
            f"Fichier source introuvable : {FICHIER_SOURCE}"
        )

    print("Ouverture du classeur...")
    classeur = openpyxl.load_workbook(
        FICHIER_SOURCE,
        read_only=False,
        data_only=False
    )

    rapport = {
        "fichier_source": FICHIER_SOURCE.name,
        "nombre_feuilles": len(classeur.sheetnames),
        "feuilles": []
    }

    for feuille in classeur.worksheets:
        print(f"Analyse de la feuille : {feuille.title}")
        rapport["feuilles"].append(analyser_feuille(feuille))

    # Rapport texte : uniquement des informations de structure
    lignes = [
        "RAPPORT DE CONTROLE QUALITE STRUCTUREL",
        "=" * 50,
        f"Fichier : {FICHIER_SOURCE.name}",
        f"Nombre de feuilles : {len(classeur.sheetnames)}",
        "",
        "AUCUNE VALEUR STATISTIQUE BRUTE N'EST RESTITUEE.",
        ""
    ]

    for feuille in rapport["feuilles"]:
        lignes.extend([
            "-" * 50,
            f"FEUILLE : {feuille['nom_feuille']}",
            f"Dimensions : {feuille['dimensions']}",
            f"Lignes non vides : {feuille['lignes_non_vides']}",
            f"Cellules vides : {feuille['cellules_vides']}",
            f"Cellules numériques : {feuille['cellules_numeriques']}",
            f"Formules : {feuille['cellules_formules']}",
            f"Lignes de total détectées : {feuille['nombre_lignes_total_detectees']}",
            f"Années détectées : {feuille['annees_detectees']}",
            f"Plages fusionnées : {feuille['plages_fusionnees']}",
            f"Libellés repérés : {feuille['libelles_reperes']}",
            f"Libellés répétés : {feuille['libelles_repetes']}",
            f"Aperçu des textes : {feuille['aperçu_entetes_textuels']}",
            ""
        ])

    FICHIER_RAPPORT.write_text(
        "\n".join(lignes),
        encoding="utf-8"
    )

    FICHIER_JSON.write_text(
        json.dumps(rapport, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    classeur.close()

    print("\nCONTROLE TERMINE")
    print(f"Rapport texte : {FICHIER_RAPPORT}")
    print(f"Rapport JSON : {FICHIER_JSON}")
    print("Le classeur original n'a pas été modifié.")


if __name__ == "__main__":
    main()
