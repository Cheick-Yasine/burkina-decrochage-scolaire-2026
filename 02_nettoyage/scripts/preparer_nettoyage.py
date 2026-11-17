
from pathlib import Path
import json
import openpyxl

PROJET = Path(__file__).resolve().parents[2]

SOURCE = (
    PROJET
    / "data"
    / "raw"
    / "DONNEES_STATISTIQUES_PRESCOLAIRE_PRIMAIRE_2016_2025.xlsx"
)

RAPPORTS = PROJET / "documentation" / "rapports"
RAPPORTS.mkdir(parents=True, exist_ok=True)

wb = openpyxl.load_workbook(
    SOURCE,
    read_only=True,
    data_only=True
)

rapport = {
    "objectif": "Examen des libelles et dimensions des tableaux",
    "feuilles": {}
}

for nom in wb.sheetnames:
    feuille = wb[nom]

    informations = {
        "libelles_textuels": [],
        "lignes_non_vides": 0,
        "colonnes_utilisees": 0
    }

    colonnes_utilisees = set()

    for numero_ligne, ligne in enumerate(feuille.iter_rows(), start=1):
        cellules_ligne = []

        for cellule in ligne:
            valeur = cellule.value

            if valeur is not None:
                colonnes_utilisees.add(cellule.column)

                if isinstance(valeur, str):
                    texte = valeur.strip()

                    if texte:
                        cellules_ligne.append({
                            "cellule": cellule.coordinate,
                            "libelle": texte
                        })

        if cellules_ligne:
            informations["lignes_non_vides"] += 1

            # Limiter le rapport aux 80 premiers libellés par feuille
            if len(informations["libelles_textuels"]) < 80:
                informations["libelles_textuels"].extend(
                    cellules_ligne
                )

    informations["colonnes_utilisees"] = len(colonnes_utilisees)

    rapport["feuilles"][nom] = informations

wb.close()

sortie = RAPPORTS / "libelles_tableaux.json"

sortie.write_text(
    json.dumps(rapport, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("EXAMEN DES LIBELLES TERMINE")
print("Nombre de feuilles :", len(rapport["feuilles"]))

for nom, infos in rapport["feuilles"].items():
    print(
        f"{nom} : "
        f"{infos['lignes_non_vides']} lignes non vides, "
        f"{len(infos['libelles_textuels'])} libelles examines"
    )

print("Rapport :", sortie)
print("Les valeurs statistiques numeriques ne sont pas affichees.")
