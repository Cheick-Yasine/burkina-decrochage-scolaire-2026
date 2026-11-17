
from pathlib import Path
import json
import openpyxl

PROJET = Path(__file__).resolve().parents[2]
SOURCE = PROJET / "data" / "raw" / "DONNEES_STATISTIQUES_PRESCOLAIRE_PRIMAIRE_2016_2025.xlsx"
RAPPORTS = PROJET / "documentation" / "rapports"
RAPPORTS.mkdir(parents=True, exist_ok=True)

# Deux ouvertures : formules et résultats enregistrés.
wb_formules = openpyxl.load_workbook(SOURCE, data_only=False)
wb_resultats = openpyxl.load_workbook(SOURCE, data_only=True)

rapport = {
    "feuilles_formules": {},
    "feuil9_entetes": []
}

for nom in ["Feuil10", "Feuil11", "Feuil12"]:
    feuille_f = wb_formules[nom]
    feuille_v = wb_resultats[nom]

    total = 0
    resultats_absents = 0
    resultats_presents = 0

    for ligne in feuille_f.iter_rows():
        for cellule in ligne:
            if isinstance(cellule.value, str) and cellule.value.startswith("="):
                total += 1
                valeur = feuille_v[cellule.coordinate].value

                if valeur is None:
                    resultats_absents += 1
                else:
                    resultats_presents += 1

    rapport["feuilles_formules"][nom] = {
        "nombre_formules": total,
        "resultats_enregistres_absents": resultats_absents,
        "resultats_enregistres_presents": resultats_presents
    }

# Examiner les types et formats des cellules de Feuil9,
# sans afficher les valeurs statistiques.
feuille = wb_formules["Feuil9"]

for ligne in range(1, min(feuille.max_row, 8) + 1):
    cellules = []
    for colonne in range(1, min(feuille.max_column, 12) + 1):
        cellule = feuille.cell(ligne, colonne)
        if cellule.value is not None:
            cellules.append({
                "cellule": cellule.coordinate,
                "type": type(cellule.value).__name__,
                "format": cellule.number_format,
                "est_date": cellule.is_date
            })

    rapport["feuil9_entetes"].append({
        "ligne": ligne,
        "cellules": cellules
    })

sortie = RAPPORTS / "verification_formules.json"
sortie.write_text(
    json.dumps(rapport, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

wb_formules.close()
wb_resultats.close()

print("VERIFICATION TERMINEE")
for nom, infos in rapport["feuilles_formules"].items():
    print(f"\n{nom}")
    print("Formules :", infos["nombre_formules"])
    print("Résultats enregistrés absents :", infos["resultats_enregistres_absents"])
    print("Résultats enregistrés présents :", infos["resultats_enregistres_presents"])

print("\nFeuil9 : types et formats des cellules d'en-tête enregistrés.")
print("Rapport :", sortie)
print("Aucune valeur statistique brute n'a été affichée.")
