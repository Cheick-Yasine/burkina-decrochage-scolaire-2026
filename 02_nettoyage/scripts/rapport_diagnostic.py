
from pathlib import Path
from datetime import datetime
import json

# Chemins du projet
PROJET = Path(__file__).resolve().parents[2]
RAPPORTS = PROJET / "documentation" / "rapports"

# Rapports déjà produits
fichiers = {
    "inventaire_initial": RAPPORTS / "inventaire_initial.json",
    "controle_qualite_structure": RAPPORTS / "controle_qualite_structure.json",
    "verification_formules": RAPPORTS / "verification_formules.json",
    "structure_feuilles": RAPPORTS / "structure_feuilles.txt"
}

diagnostic = {
    "date_diagnostic": datetime.now().isoformat(timespec="seconds"),
    "fichier_source": "DONNEES_STATISTIQUES_PRESCOLAIRE_PRIMAIRE_2016_2025.xlsx",
    "rapports": {},
    "fichiers_absents": []
}

# Lecture des rapports existants
for nom, chemin in fichiers.items():
    if not chemin.exists():
        diagnostic["fichiers_absents"].append(nom)
        continue

    if chemin.suffix == ".json":
        with chemin.open("r", encoding="utf-8") as fichier:
            diagnostic["rapports"][nom] = json.load(fichier)
    else:
        diagnostic["rapports"][nom] = chemin.read_text(
            encoding="utf-8"
        )

# Enregistrement du diagnostic consolidé
sortie_json = RAPPORTS / "diagnostic_consolide.json"

sortie_json.write_text(
    json.dumps(diagnostic, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

# Création du rapport lisible
lignes = [
    "RAPPORT DE DIAGNOSTIC CONSOLIDE",
    "=" * 50,
    "",
    f"Date : {diagnostic['date_diagnostic']}",
    f"Fichier source : {diagnostic['fichier_source']}",
    "",
    "1. RAPPORTS DISPONIBLES",
    "-" * 50
]

for nom in diagnostic["rapports"]:
    lignes.append(f"[OK] {nom}")

if diagnostic["fichiers_absents"]:
    lignes.extend([
        "",
        "2. RAPPORTS ABSENTS",
        "-" * 50
    ])
    for nom in diagnostic["fichiers_absents"]:
        lignes.append(f"[ABSENT] {nom}")

lignes.extend([
    "",
    "3. CONTENU DES RAPPORTS DE CONTROLE",
    "-" * 50
])

for nom, contenu in diagnostic["rapports"].items():
    lignes.extend(["", f"--- {nom} ---", ""])

    if isinstance(contenu, dict):
        lignes.append(
            json.dumps(contenu, ensure_ascii=False, indent=2)
        )
    else:
        lignes.append(contenu)

lignes.extend([
    "",
    "=" * 50,
    "Fin du diagnostic.",
    "Le classeur Excel original n'a pas été modifié."
])

sortie_txt = RAPPORTS / "diagnostic_consolide.txt"
sortie_txt.write_text("\n".join(lignes), encoding="utf-8")

print("DIAGNOSTIC CONSOLIDE TERMINE")
print("Rapports disponibles :", len(diagnostic["rapports"]))
print("Rapports absents :", len(diagnostic["fichiers_absents"]))
print("Fichier JSON :", sortie_json)
print("Fichier TXT :", sortie_txt)
print("Le classeur Excel original reste intact.")
