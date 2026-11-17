
from pathlib import Path
import json

PROJET = Path(__file__).resolve().parents[2]
SOURCE = PROJET / "documentation" / "rapports" / "libelles_tableaux.json"

with SOURCE.open("r", encoding="utf-8") as fichier:
    rapport = json.load(fichier)

termes_a_exclure = [
    "automated assistant",
    "automated assistant (ai)",
    "traceability",
    "provided to you",
    "do not send",
    "for any automated",
]

print("LIBELLES UTILES PAR FEUILLE")
print("=" * 60)

for nom, infos in rapport["feuilles"].items():
    libelles = set()

    for element in infos["libelles_textuels"]:
        texte = element["libelle"].strip()
        texte_min = texte.lower()

        if len(texte) > 60:
            continue

        if any(terme in texte_min for terme in termes_a_exclure):
            continue

        if texte:
            libelles.add(texte)

    print(f"\n--- {nom} ---")

    for libelle in sorted(libelles):
        print("-", libelle)

print("\nEXTRACTION TERMINEE")
print("Aucune valeur statistique numérique n'a été affichée.")
