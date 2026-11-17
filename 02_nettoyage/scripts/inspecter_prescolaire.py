
from pathlib import Path
import json

PROJET = Path(__file__).resolve().parents[2]

SOURCE = (
    PROJET / "documentation" / "rapports"
    / "structure_lignes.json"
)

SORTIE = (
    PROJET / "documentation" / "rapports"
    / "detail_prescolaire.txt"
)

structure = json.loads(
    SOURCE.read_text(encoding="utf-8")
)

termes_a_exclure = [
    "automated assistant",
    "traceability",
    "provided to you",
    "do not send",
    "if you read this note",
    "for any automated"
]

lignes = structure.get("PRESCOLAIRE")

if lignes is None:
    raise ValueError("Feuille PRESCOLAIRE introuvable.")

rapport = [
    "DETAIL DE LA FEUILLE PRESCOLAIRE",
    "Libelles textuels uniquement",
    ""
]

for ligne in lignes:
    libelles = []

    for element in ligne["libelles"]:
        texte = element["libelle"].strip()

        if len(texte) > 80:
            continue

        if any(mot in texte.lower() for mot in termes_a_exclure):
            continue

        libelles.append(
            f"{element['cellule']} : {texte}"
        )

    if libelles:
        rapport.append(
            f"Ligne {ligne['numero_ligne']} : "
            + " | ".join(libelles)
        )

SORTIE.write_text(
    "\n".join(rapport),
    encoding="utf-8"
)

print("INSPECTION PRESCOLAIRE TERMINEE")
print("Nombre de lignes examinees :", len(lignes))
print("Rapport :", SORTIE)
print("Aucune valeur statistique affichee.")
