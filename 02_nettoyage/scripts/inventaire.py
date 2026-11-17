
from pathlib import Path
import json
from openpyxl import load_workbook

# Chemin du projet
ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"
RAPPORTS = ROOT / "documentation" / "rapports"

# Créer le dossier des rapports s'il n'existe pas
RAPPORTS.mkdir(parents=True, exist_ok=True)

# Sélectionner le fichier Excel attendu
FICHIER = DATA_RAW / "DONNEES_STATISTIQUES_PRESCOLAIRE_PRIMAIRE_2016_2025.xlsx"

if not FICHIER.is_file():
    raise FileNotFoundError(f"Fichier introuvable : {FICHIER}")

print(f"Fichier analysé : {FICHIER.name}")
print("Ouverture du classeur...")

# Lecture seule : le fichier original ne sera pas modifié
wb = load_workbook(FICHIER, read_only=True, data_only=False)

inventaire = {
    "fichier": FICHIER.name,
    "nombre_feuilles": len(wb.sheetnames),
    "feuilles": []
}

for ws in wb.worksheets:
    lignes_non_vides = 0
    cellules_non_vides = 0
    formules = 0
    colonnes_utilisees = set()

    for ligne in ws.iter_rows():
        ligne_contient_donnees = False

        for cellule in ligne:
            if cellule.value is not None:
                cellules_non_vides += 1
                colonnes_utilisees.add(cellule.column)
                ligne_contient_donnees = True

                if isinstance(cellule.value, str) and cellule.value.startswith("="):
                    formules += 1

        if ligne_contient_donnees:
            lignes_non_vides += 1

    inventaire["feuilles"].append({
        "nom": ws.title,
        "lignes_max": ws.max_row,
        "colonnes_max": ws.max_column,
        "lignes_non_vides": lignes_non_vides,
        "cellules_non_vides": cellules_non_vides,
        "colonnes_utilisees": sorted(colonnes_utilisees),
        "nombre_formules": formules
    })

wb.close()

# Enregistrer les résultats
fichier_json = RAPPORTS / "inventaire_initial.json"
fichier_txt = RAPPORTS / "inventaire_initial.txt"

with open(fichier_json, "w", encoding="utf-8") as f:
    json.dump(inventaire, f, ensure_ascii=False, indent=4)

with open(fichier_txt, "w", encoding="utf-8") as f:
    f.write(f"INVENTAIRE DU CLASSEUR : {FICHIER.name}\n")
    f.write(f"Nombre de feuilles : {inventaire['nombre_feuilles']}\n\n")

    for feuille in inventaire["feuilles"]:
        f.write(f"FEUILLE : {feuille['nom']}\n")
        f.write(f"Lignes maximales : {feuille['lignes_max']}\n")
        f.write(f"Colonnes maximales : {feuille['colonnes_max']}\n")
        f.write(f"Lignes non vides : {feuille['lignes_non_vides']}\n")
        f.write(f"Cellules non vides : {feuille['cellules_non_vides']}\n")
        f.write(f"Colonnes utilisées : {feuille['colonnes_utilisees']}\n")
        f.write(f"Formules : {feuille['nombre_formules']}\n\n")

print("\nINVENTAIRE TERMINÉ")
print(f"Nombre de feuilles : {inventaire['nombre_feuilles']}")

for feuille in inventaire["feuilles"]:
    print(
        f"- {feuille['nom']} : "
        f"{feuille['lignes_non_vides']} lignes non vides, "
        f"{feuille['cellules_non_vides']} cellules non vides"
    )

print(f"\nRapport JSON : {fichier_json}")
print(f"Rapport texte : {fichier_txt}")
