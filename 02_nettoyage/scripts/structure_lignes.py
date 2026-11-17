
from pathlib import Path
import json
import openpyxl

PROJET = Path(__file__).resolve().parents[2]

SOURCE = (
    PROJET / "data" / "raw"
    / "DONNEES_STATISTIQUES_PRESCOLAIRE_PRIMAIRE_2016_2025.xlsx"
)

RAPPORTS = PROJET / "documentation" / "rapports"
RAPPORTS.mkdir(parents=True, exist_ok=True)

wb = openpyxl.load_workbook(
    SOURCE,
    read_only=True,
    data_only=True
)

termes_interdits = [
    "automated assistant",
    "traceability",
    "provided to you",
    "do not send",
    "for any automated",
    "if you read this note"
]

rapport = {}

for nom in wb.sheetnames:
    feuille = wb[nom]
    lignes = []

    for numero, ligne in enumerate(
        feuille.iter_rows(min_col=1, max_col=3),
        start=1
    ):
        libelles = []

        for cellule in ligne:
            valeur = cellule.value

            if isinstance(valeur, str):
                texte = valeur.strip()

                if not texte or len(texte) > 80:
                    continue

                if any(
                    terme in texte.lower()
                    for terme in termes_interdits
                ):
                    continue

                libelles.append({
                    "cellule": cellule.coordinate,
                    "libelle": texte
                })

        if libelles:
            lignes.append({
                "numero_ligne": numero,
                "libelles": libelles
            })

    rapport[nom] = lignes

wb.close()

sortie = RAPPORTS / "structure_lignes.json"

sortie.write_text(
    json.dumps(rapport, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("STRUCTURE DES LIGNES TERMINEE")
print("Feuilles examinees :", len(rapport))

for nom, lignes in rapport.items():
    print(f"{nom} : {len(lignes)} lignes avec libelles")

print("Rapport :", sortie)
print("Aucune valeur statistique numerique affichee.")
