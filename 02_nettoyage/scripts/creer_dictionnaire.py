
from pathlib import Path
import json
import re
import unicodedata

PROJET = Path(__file__).resolve().parents[2]

SOURCE = (
    PROJET / "documentation" / "rapports"
    / "structure_lignes.json"
)

DOSSIER = PROJET / "documentation" / "dictionnaire"
DOSSIER.mkdir(parents=True, exist_ok=True)

INDICATEURS = {
    "PRESCOLAIRE": {
        "indicateur": "Effectifs du préscolaire",
        "dimensions": ["Région", "Sexe", "Statut", "Milieu", "Niveau"]
    },
    "Feuil1": {
        "indicateur": "Effectifs du primaire",
        "dimensions": ["Région", "Sexe"]
    },
    "Feuil2": {
        "indicateur": "Effectifs par statut",
        "dimensions": ["Statut public/privé", "Sexe"]
    },
    "Feuil3": {
        "indicateur": "Effectifs par milieu",
        "dimensions": ["Milieu urbain/rural", "Sexe"]
    },
    "Feuil4": {
        "indicateur": "Effectifs par niveau scolaire",
        "dimensions": ["Niveau", "Sexe", "Statut"]
    },
    "Feuil5": {
        "indicateur": "Nouveaux entrants au CP1",
        "dimensions": ["Région", "Sexe"]
    },
    "Feuil6": {
        "indicateur": "Taux brut d'admission (TBA)",
        "dimensions": ["Région", "Sexe"]
    },
    "Feuil7": {
        "indicateur": "Taux brut de scolarisation (TBS)",
        "dimensions": ["Région", "Sexe"]
    },
    "Feuil8": {
        "indicateur": "Taux d'achèvement du primaire (TAP)",
        "dimensions": ["Région", "Sexe"]
    },
    "Feuil9": {
        "indicateur": "Taux de réussite au CEP",
        "dimensions": ["Région", "Sexe"]
    },
    "Feuil10": {
        "indicateur": "Indice de parité du TBA",
        "dimensions": ["Région"]
    },
    "Feuil11": {
        "indicateur": "Indice de parité du TBS",
        "dimensions": ["Région"]
    },
    "Feuil12": {
        "indicateur": "Indice de parité du TAP",
        "dimensions": ["Région"]
    },
    "Feuil13": {
        "indicateur": "Nombre d'écoles primaires",
        "dimensions": ["Région", "Statut"]
    }
}

REGIONS = {
    "BOUCLE DU MOUHOUN",
    "CASCADES",
    "CENTRE",
    "CENTRE EST",
    "CENTRE NORD",
    "CENTRE OUEST",
    "CENTRE SUD",
    "EST",
    "HAUTS BASSINS",
    "HAUT BASSINS",
    "NORD",
    "PLATEAU CENTRAL",
    "SAHEL",
    "SUD OUEST"
}

def normaliser(texte):
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(
        c for c in texte if not unicodedata.combining(c)
    )
    return " ".join(
        re.sub(r"[^A-Z0-9 ]", " ", texte.upper()).split()
    )

if not SOURCE.exists():
    raise FileNotFoundError(
        f"Rapport introuvable : {SOURCE}"
    )

structure = json.loads(
    SOURCE.read_text(encoding="utf-8")
)

dictionnaire = {}

for feuille, lignes in structure.items():
    infos = INDICATEURS.get(feuille, {
        "indicateur": "À préciser",
        "dimensions": []
    })

    lignes_regions = []
    lignes_nationales = []
    lignes_totaux = []
    annees = set()

    for ligne in lignes:
        numero = ligne["numero_ligne"]
        libelles = [
            element["libelle"]
            for element in ligne["libelles"]
        ]

        textes = [normaliser(x) for x in libelles]

        for texte in libelles:
            correspondances = re.findall(
                r"20\d{2}\s*[/\-]\s*(?:20)?\d{2}",
                texte
            )
            annees.update(
                re.sub(r"\s+", "", annee)
                for annee in correspondances
            )

        if any(texte in REGIONS for texte in textes):
            lignes_regions.append(numero)

        if any(
            "NATIONAL" in texte
            or "BURKINA FASO" in texte
            for texte in textes
        ):
            lignes_nationales.append(numero)

        if any(
            texte == "TOTAL"
            or texte.startswith("TOTAL GENERAL")
            or texte.startswith("TOTAL NATIONAL")
            for texte in textes
        ):
            lignes_totaux.append(numero)

    periode = sorted(annees)

    if feuille == "Feuil9":
        periode = ["2016 à 2025 (en-têtes numériques)"]

    dictionnaire[feuille] = {
        "indicateur": infos["indicateur"],
        "dimensions": infos["dimensions"],
        "periode_identifiee": periode,
        "nombre_lignes_avec_libelles": len(lignes),
        "lignes_regions_candidates": lignes_regions,
        "lignes_nationales_candidates": lignes_nationales,
        "lignes_totaux_candidates": lignes_totaux,
        "verification_manuelle_requise": True
    }

fichier_json = DOSSIER / "dictionnaire_donnees.json"
fichier_txt = DOSSIER / "dictionnaire_donnees.txt"

fichier_json.write_text(
    json.dumps(dictionnaire, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

rapport = [
    "DICTIONNAIRE DE DONNEES",
    "Projet : Cartographie du risque de decrochage scolaire",
    "",
    "Attention : les lignes candidates doivent etre verifiees",
    "avant toute transformation ou suppression de donnees.",
    ""
]

for feuille, infos in dictionnaire.items():
    rapport.extend([
        f"FEUILLE : {feuille}",
        f"Indicateur : {infos['indicateur']}",
        f"Dimensions : {', '.join(infos['dimensions'])}",
        f"Periode : {', '.join(infos['periode_identifiee']) or 'A confirmer'}",
        f"Lignes avec libelles : {infos['nombre_lignes_avec_libelles']}",
        f"Lignes regionales candidates : {len(infos['lignes_regions_candidates'])}",
        f"Lignes nationales candidates : {len(infos['lignes_nationales_candidates'])}",
        f"Lignes de totaux candidates : {len(infos['lignes_totaux_candidates'])}",
        ""
    ])

fichier_txt.write_text(
    "\n".join(rapport),
    encoding="utf-8"
)

print("DICTIONNAIRE CREE AVEC SUCCES")
print("Feuilles documentees :", len(dictionnaire))
print("Fichier JSON :", fichier_json)
print("Fichier texte :", fichier_txt)
print("Aucune valeur statistique numerique affichee.")
print("Les lignes candidates devront etre verifiees avant nettoyage.")
