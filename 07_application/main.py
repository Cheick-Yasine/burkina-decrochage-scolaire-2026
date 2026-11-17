from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
DATA_FILE = ROOT / "data" / "processed" / "indicateurs_primaire.csv"

app = FastAPI(
    title="Vigie École",
    description="Observatoire territorial de la vigilance scolaire au Burkina Faso.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Fichier absent : data/processed/indicateurs_primaire.csv. "
            "Exécute d'abord le script de transformation."
        )
    df = pd.read_csv(DATA_FILE)
    required = {"region", "indicateur", "periode", "valeur", "dimension", "modalite"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes dans le fichier traité : {', '.join(sorted(missing))}")
    df["valeur"] = pd.to_numeric(df["valeur"], errors="coerce")
    df = df.dropna(subset=["valeur"]).copy()
    for col in ("region", "indicateur", "periode", "dimension", "modalite"):
        df[col] = df[col].fillna("Non précisé").astype(str)
    return df


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "Vigie École"}


@app.get("/api/metadata")
def metadata() -> dict[str, Any]:
    try:
        df = load_data()
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {
        "observations": int(len(df)),
        "regions": sorted(df["region"].unique().tolist()),
        "indicators": sorted(df["indicateur"].unique().tolist()),
        "dimensions": sorted(df["dimension"].unique().tolist()),
        "periods": sorted(df["periode"].unique().tolist()),
        "source": "DGESS · Données statistiques préscolaire et primaire 2016–2025",
        "scope": "Primaire · 13 anciennes régions",
    }


@app.get("/api/observations")
def observations(
    indicator: str = Query(..., min_length=1),
    dimension: str | None = None,
    modality: str | None = None,
    periods: list[str] | None = Query(default=None),
    regions: list[str] | None = Query(default=None),
) -> dict[str, Any]:
    try:
        df = load_data()
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    df = df[df["indicateur"] == indicator]
    if dimension:
        df = df[df["dimension"] == dimension]
    if modality:
        df = df[df["modalite"] == modality]
    if periods:
        df = df[df["periode"].isin(periods)]
    if regions:
        df = df[df["region"].isin(regions)]

    keys = [c for c in ("cycle", "region", "indicateur", "periode", "dimension", "modalite") if c in df.columns]
    duplicate_count = int(df.duplicated(subset=keys, keep=False).sum()) if keys else 0
    unit = str(df["unite"].dropna().iloc[0]) if "unite" in df and not df["unite"].dropna().empty else ""
    rows = []
    for row in df.to_dict(orient="records"):
        rows.append({
            "region": str(row["region"]),
            "periode": str(row["periode"]),
            "valeur": float(row["valeur"]),
            "modalite": str(row["modalite"]),
            "dimension": str(row["dimension"]),
            "unite": str(row.get("unite", "")),
            "type_periode": str(row.get("type_periode", "")),
        })
    return {
        "rows": rows,
        "unit": unit,
        "duplicate_rows": duplicate_count,
        "count": len(rows),
    }
