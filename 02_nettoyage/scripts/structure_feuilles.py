
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[2]
FICHIER = ROOT / "data" / "raw" / "DONNEES_STATISTIQUES_PRESCOLAIRE_PRIMAIRE_2016_2025.xlsx"
SORTIE = ROOT / "documentation" / "rapports" / "structure_feuilles.txt"

wb = load_workbook(FICHIER, read_only=True, data_only=False)

with open(SORTIE, "w", encoding="utf-8") as rapport:
    for ws in wb.worksheets:
        rapport.write(f"\n{'=' * 60}\n")
        rapport.write(f"FEUILLE : {ws.title}\n")
        rapport.write(f"{'=' * 60}\n")

        lignes_lues = 0
        for numero, ligne in enumerate(ws.iter_rows(max_row=12, max_col=15), start=1):
            elements = []

            for cellule in ligne:
                valeur = cellule.value

                if valeur is None:
                    continue
                elif isinstance(valeur, str) and valeur.startswith("="):
                    affichage = "[FORMULE]"
                elif isinstance(valeur, str):
                    affichage = valeur.strip()
                else:
                    affichage = "[VALEUR NUMERIQUE OU DATE]"

                elements.append(f"{get_column_letter(cellule.column)}={affichage}")

            if elements:
                rapport.write(f"Ligne {numero} : {' | '.join(elements)}\n")
                lignes_lues += 1

            if lignes_lues >= 8:
                break

wb.close()
print(f"Aperçu créé : {SORTIE}")
