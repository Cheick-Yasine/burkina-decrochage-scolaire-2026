
from pathlib import Path
import json
import unicodedata
import re

PROJET = Path(__file__).resolve().parents[2]

SOURCE = (
    PROJET / "documentation" / "rapports"
    / "structure_lignes.json"
)

SORTIE = (
    PROJET / "documentation" / "rapports"
    / "verification_lignes_candidates.txt"
)

REGIONS = {
    "BOUCLE DU MOUHOUN", "CASCADES", "CENTRE",
    "CENTRE EST", "CENTRE NORD", "CENTRE OUEST",
    "CENTRE SUD", "EST", "HAUTS BASSINS",
    "HAUT BASSINS", "NORD", "PLATEAU CENTRAL",
    "SAHEL", "SUD OUEST"
}

def normaliser(texte):
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(
        c for c in texte if not unicodedata.combining(c)
    )
    return " ".join(
        re.sub(r"[^A-Z0-9 ]", " ", texte.upper()).split()
    )

structure = json.loads(SOURCE.read_text(encoding="utf-8"))

rapport = [
    "VERIFICATION DES LIGNES CANDIDATES",
    "Libelles uniquement - aucune valeur statistique",
    ""
]

for feuille, lignes in structure.items():
    rapport.append(f"\n===== {feuille} =====")

    for ligne in lignes:
        libelles = [
            element["libelle"]
            for element in ligne["libelles"]
        ]

        textes = [normaliser(x) for x in libelles]

        categories = []

        if any(x in REGIONS for x in textes):
            categories.append("REGION")

        if any(
            "NATIONAL" in x or "BURKINA FASO" in x
            for x in textes
        ):
            categories.append("NATIONAL")

        if any(
            x == "TOTAL"
            or x.startswith("TOTAL GENERAL")
            or x.startswith("TOTAL NATIONAL")
            for x in textes
        ):
            categories.append("TOTAL")

        if categories:
            # On ne conserve que les libelles courts et textuels.
            libelles_surs = [
                x for x in libelles
                if len(x) <= 80
                and not any(
                    terme in x.lower()
                    for terme in [
                        "automated assistant",
                        "traceability",
                        "provided to you",
                        "do not send"
                    ]
                )
            ]

            rapport.append(
                f"Ligne {ligne['numero_ligne']} "
                f"[{', '.join(categories)}] : "
                f"{' | '.join(libelles_surs)}"
            )

SORTIE.write_text(
    "\n".join(rapport),
    encoding="utf-8"
)

print("VERIFICATION TERMINEE")
print("Rapport :", SORTIE)
print("Aucune valeur statistique numerique affichee.")
