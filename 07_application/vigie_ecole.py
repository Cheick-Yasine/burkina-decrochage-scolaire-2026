from __future__ import annotations

from pathlib import Path
import re
import unicodedata

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------
# VIGIE ÉCOLE — interface de démonstration connectée aux données locales
# Aucun chiffre n'est simulé : tous les indicateurs viennent du CSV traité.
# ---------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "processed" / "indicateurs_primaire.csv"

st.set_page_config(
    page_title="Vigie École | Burkina Faso",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#10243A"
BLUE = "#1E5EFF"
CYAN = "#39B7C8"
GOLD = "#E9B44C"
INK = "#172B3A"
MUTED = "#718096"
PAPER = "#F4F7FB"
WHITE = "#FFFFFF"
RED = "#D65A5A"
GREEN = "#168A70"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root {{ --navy:{NAVY}; --blue:{BLUE}; --paper:{PAPER}; }}
    html, body, [class*="css"] {{ font-family:'DM Sans',sans-serif; }}
    .stApp {{ background:var(--paper); }}
    [data-testid="stHeader"] {{ background:rgba(244,247,251,.92); }}
    [data-testid="stSidebar"] {{ background:{NAVY}; border-right:1px solid #233B54; }}
    [data-testid="stSidebar"] * {{ color:#EAF1F8 !important; }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color:#AFC1D2 !important; }}
    [data-testid="stSidebar"] .stRadio label {{ padding:7px 10px; border-radius:9px; }}
    [data-testid="stSidebar"] .stRadio label:hover {{ background:#203B56; }}
    [data-testid="stSidebar"] hr {{ border-color:#29445F; }}
    .block-container {{ padding-top:1.5rem; padding-bottom:3rem; max-width:1500px; }}
    h1,h2,h3 {{ font-family:'Manrope',sans-serif; color:{INK}; letter-spacing:-.035em; }}
    .brand {{ display:flex; align-items:center; gap:10px; margin:4px 0 24px; }}
    .brand-mark {{ width:42px;height:42px;border-radius:13px;background:linear-gradient(145deg,{BLUE},{CYAN});display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 8px 22px #07192d55; }}
    .brand-name {{ font-family:'Manrope',sans-serif;font-size:19px;font-weight:800;color:white;letter-spacing:-.6px; }}
    .brand-sub {{ color:#9DB2C7;font-size:10px;letter-spacing:1.7px;text-transform:uppercase; }}
    .side-label {{ color:#7891A8;font-size:10px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;margin:22px 0 8px; }}
    .hero {{ background:linear-gradient(115deg,#10243A 0%,#173C5A 65%,#1D5870 100%);border-radius:22px;padding:27px 30px;color:white;position:relative;overflow:hidden;margin-bottom:22px; }}
    .hero:after {{ content:"";position:absolute;width:300px;height:300px;border:1px solid #ffffff18;border-radius:50%;right:-80px;top:-170px;box-shadow:0 0 0 35px #ffffff08,0 0 0 75px #ffffff05; }}
    .eyebrow {{ font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#80D4DD;font-weight:700;margin-bottom:10px; }}
    .hero-title {{ font-family:'Manrope',sans-serif;font-size:clamp(25px,3vw,38px);line-height:1.12;font-weight:800;letter-spacing:-1.3px;color:white;margin:0 0 10px;max-width:760px; }}
    .hero-copy {{ color:#C0D1DF;font-size:14px;max-width:720px;line-height:1.6;margin:0; }}
    .hero-chip {{ display:inline-block;border:1px solid #ffffff35;border-radius:30px;padding:6px 11px;font-size:10px;color:#D9E7F2;margin-top:18px; }}
    .section-kicker {{ color:{BLUE};font-size:10px;font-weight:800;letter-spacing:1.8px;text-transform:uppercase;margin:5px 0 5px; }}
    .section-title {{ font-family:'Manrope',sans-serif;color:{INK};font-size:21px;font-weight:800;letter-spacing:-.6px;margin:0 0 4px; }}
    .section-desc {{ color:{MUTED};font-size:12px;margin:0 0 14px; }}
    .metric-card {{ background:white;border:1px solid #E5EBF2;border-radius:16px;padding:17px 18px;min-height:118px;box-shadow:0 4px 14px #142b4307; }}
    .metric-label {{ color:#77879A;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.1px; }}
    .metric-value {{ font-family:'Manrope',sans-serif;font-size:27px;font-weight:800;letter-spacing:-1px;color:{INK};margin:8px 0 2px; }}
    .metric-foot {{ color:#8A99A8;font-size:10px; }}
    .panel {{ background:white;border:1px solid #E5EBF2;border-radius:17px;padding:17px 19px;box-shadow:0 4px 14px #142b4307; }}
    .note {{ background:#EDF5FC;border-left:3px solid {BLUE};border-radius:8px;padding:11px 13px;color:#476176;font-size:12px;line-height:1.55; }}
    .warning {{ background:#FFF7E8;border-left:3px solid {GOLD};border-radius:8px;padding:11px 13px;color:#745A2A;font-size:12px;line-height:1.55; }}
    .footer {{ color:#92A0AE;font-size:10px;border-top:1px solid #E4EAF0;padding-top:14px;margin-top:35px; }}
    div[data-testid="stSelectbox"] label, div[data-testid="stMultiSelect"] label {{ color:#637488;font-size:11px;font-weight:700; }}
    .stTabs [data-baseweb="tab-list"] {{ gap:8px; }}
    .stTabs [data-baseweb="tab"] {{ background:#EAF0F6;border-radius:9px 9px 0 0;padding:9px 15px; }}
    .stTabs [aria-selected="true"] {{ background:white; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def norm(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", text).strip().lower()


def period_key(value: object) -> tuple[int, str]:
    match = re.search(r"(20\d{2})", str(value))
    return (int(match.group(1)) if match else 9999, str(value))


def fmt(value: float, unit: str) -> str:
    if pd.isna(value):
        return "—"
    if unit == "pourcentage" or "%" in unit.lower():
        return f"{value:,.1f} %".replace(",", " ")
    if unit == "effectif":
        return f"{value:,.0f}".replace(",", " ")
    return f"{value:,.2f}".replace(",", " ")


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        return pd.DataFrame()
    frame = pd.read_csv(DATA_FILE)
    required = {"region", "indicateur", "periode", "valeur", "dimension", "modalite"}
    if not required.issubset(frame.columns):
        raise ValueError("Le fichier d'indicateurs ne possède pas toutes les colonnes attendues.")
    frame["valeur"] = pd.to_numeric(frame["valeur"], errors="coerce")
    frame = frame.dropna(subset=["valeur"]).copy()
    frame["periode"] = frame["periode"].astype(str)
    frame["region"] = frame["region"].astype(str)
    frame["indicateur"] = frame["indicateur"].astype(str)
    frame["modalite"] = frame["modalite"].fillna("Ensemble").astype(str)
    frame["dimension"] = frame["dimension"].fillna("Aucune").astype(str)
    return frame


# Sidebar identity and navigation
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
          <div class="brand-mark">◈</div>
          <div><div class="brand-name">VIGIE ÉCOLE</div><div class="brand-sub">Burkina Faso · Data for action</div></div>
        </div>
        <div class="side-label">Espace d'exploration</div>
        """,
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Navigation",
        ["Vue d'ensemble", "Explorer les territoires", "Suivre les évolutions", "Qualité & méthode"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown('<div class="side-label">Périmètre des données</div>', unsafe_allow_html=True)

try:
    df = load_data()
except Exception as exc:
    df = pd.DataFrame()
    load_error = str(exc)
else:
    load_error = ""

if df.empty:
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">Observatoire de la vigilance scolaire</div>
          <div class="hero-title">Voir les signaux faibles.<br>Agir avant la rupture.</div>
          <p class="hero-copy">Vigie École transforme les statistiques scolaires en repères lisibles pour comprendre les disparités territoriales et éclairer l'action.</p>
          <span class="hero-chip">BURKINA FASO · ÉDITION 2026</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if load_error:
        st.error(load_error)
    else:
        st.warning("Le fichier traité n'a pas été trouvé. Place le fichier indicateurs_primaire.csv dans data/processed/ puis relance l'application.")
    st.markdown("### Ce que la plateforme va rendre visible")
    c1, c2, c3 = st.columns(3)
    for col, icon, title, body in [
        (c1, "⌖", "Territoires", "Comparer les régions à partir des indicateurs réellement disponibles."),
        (c2, "↗", "Trajectoires", "Suivre les évolutions dans le temps sans confondre année scolaire et année civile."),
        (c3, "◎", "Vigilance", "Distinguer les faits observés, les signaux indirects et les risques estimés."),
    ]:
        with col:
            st.markdown(f'<div class="metric-card"><div style="font-size:24px;color:{BLUE}">{icon}</div><b>{title}</b><p style="font-size:12px;color:{MUTED}">{body}</p></div>', unsafe_allow_html=True)
    st.stop()

# Global filters
indicators = sorted(df["indicateur"].dropna().unique().tolist())
with st.sidebar:
    indicator = st.selectbox("Indicateur", indicators)
    subset_indicator = df[df["indicateur"] == indicator].copy()
    dimensions = sorted(subset_indicator["dimension"].dropna().unique().tolist())
    dimension = st.selectbox("Dimension", dimensions) if dimensions else None
    subset_dimension = subset_indicator[subset_indicator["dimension"] == dimension] if dimension else subset_indicator
    modalities = sorted(subset_dimension["modalite"].dropna().unique().tolist())
    modality = st.selectbox("Modalité", modalities) if modalities else None
    years = sorted(subset_dimension["periode"].dropna().unique().tolist(), key=period_key)
    selected_periods = st.multiselect("Périodes", years, default=years)
    regions = sorted(df["region"].dropna().unique().tolist())
    selected_regions = st.multiselect("Régions", regions, default=regions)
    st.markdown("---")
    st.markdown('<div style="font-size:10px;color:#8FA7BC">SOURCE ACTIVE</div><div style="font-size:12px;color:white;font-weight:700">DGESS · Statistiques scolaires</div><div style="font-size:10px;color:#8FA7BC">Classeur primaire 2016–2025</div>', unsafe_allow_html=True)

view = subset_dimension.copy()
if modality:
    view = view[view["modalite"] == modality]
if selected_periods:
    view = view[view["periode"].isin(selected_periods)]
if selected_regions:
    view = view[view["region"].isin(selected_regions)]
view = view.sort_values("periode", key=lambda s: s.map(lambda x: period_key(x)[0]))

# Detect logical duplicate keys; never silently aggregate contradictory source rows.
key_cols = [c for c in ["cycle", "region", "indicateur", "periode", "dimension", "modalite"] if c in view.columns]
duplicate_rows = int(view.duplicated(subset=key_cols, keep=False).sum()) if key_cols else 0
unit = str(view["unite"].dropna().iloc[0]) if "unite" in view.columns and not view["unite"].dropna().empty else ""

# Header
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Observatoire de la vigilance scolaire · Burkina Faso</div>
      <div class="hero-title">Voir les signaux faibles.<br>Agir avant la rupture.</div>
      <p class="hero-copy">Une lecture territoriale des parcours scolaires pour repérer les fragilités, suivre les trajectoires et mieux orienter les décisions.</p>
      <span class="hero-chip">DONNÉES DGESS · PRIMAIRE · 2016–2025</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(f'<div class="section-kicker">TABLEAU DE BORD · {page.upper()}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="section-title">{indicator}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="section-desc">Lecture filtrée sur {len(selected_regions)} territoire(s) et {len(selected_periods)} période(s). Les valeurs affichées proviennent du fichier traité.</div>', unsafe_allow_html=True)

if duplicate_rows:
    st.markdown(
        f'<div class="warning"><b>Contrôle qualité à terminer :</b> {duplicate_rows} lignes appartiennent à des clés territoriales répétées dans la sélection. Les comparaisons sont suspendues pour éviter de produire un classement trompeur. Corrige la source de ces doublons avant l’analyse.</div>',
        unsafe_allow_html=True,
    )
    st.stop()

if view.empty:
    st.info("Aucune observation ne correspond à cette sélection. Modifie les filtres dans le panneau de gauche.")
    st.stop()

# Overview metrics: descriptive, never mislabeled as dropout or risk.
latest_period = sorted(view["periode"].unique(), key=period_key)[-1]
latest = view[view["periode"] == latest_period]
values = latest["valeur"].dropna()
regions_count = int(latest["region"].nunique())
median_value = float(values.median()) if not values.empty else float("nan")
min_value = float(values.min()) if not values.empty else float("nan")
max_value = float(values.max()) if not values.empty else float("nan")
mean_value = float(values.mean()) if not values.empty else float("nan")

if page == "Vue d'ensemble":
    kpis = [
        ("TERRITOIRES COUVERTS", str(regions_count), "dans la période la plus récente"),
        ("PÉRIODE LA PLUS RÉCENTE", latest_period, "selon la source sélectionnée"),
        ("VALEUR MÉDIANE", fmt(median_value, unit), "médiane entre territoires"),
        ("ÉCART OBSERVÉ", fmt(max_value - min_value, unit), "maximum moins minimum"),
    ]
    cols = st.columns(4)
    for col, (label, value, foot) in zip(cols, kpis):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-foot">{foot}</div></div>', unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1.55, 1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("**Trajectoire nationale**")
        trend = view.groupby("periode", as_index=False)["valeur"].median()
        trend["periode"] = pd.Categorical(trend["periode"], categories=sorted(trend["periode"].unique(), key=period_key), ordered=True)
        trend = trend.sort_values("periode")
        fig = px.line(trend, x="periode", y="valeur", markers=True)
        fig.update_traces(line=dict(color=BLUE, width=3), marker=dict(size=8, color=CYAN))
        fig.update_layout(height=310, margin=dict(l=5,r=5,t=15,b=5), paper_bgcolor="white", plot_bgcolor="white", font=dict(family="DM Sans",color=MUTED,size=11), xaxis_title="", yaxis_title=unit, hovermode="x unified")
        fig.update_xaxes(showgrid=False, linecolor="#E8EDF3")
        fig.update_yaxes(gridcolor="#EDF1F5", zeroline=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("**Lecture territoriale · dernière période**")
        rank = latest.groupby("region", as_index=False)["valeur"].mean().sort_values("valeur", ascending=False)
        fig2 = px.bar(rank, x="valeur", y="region", orientation="h")
        fig2.update_traces(marker_color=CYAN, marker_line_width=0)
        fig2.update_layout(height=310, margin=dict(l=5,r=5,t=15,b=5), paper_bgcolor="white", plot_bgcolor="white", font=dict(family="DM Sans",color=MUTED,size=10), xaxis_title=unit, yaxis_title="", showlegend=False)
        fig2.update_xaxes(gridcolor="#EDF1F5", zeroline=False)
        fig2.update_yaxes(categoryorder="total ascending", showgrid=False)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown('<div class="note"><b>À retenir :</b> cet écran décrit l’indicateur sélectionné. Il ne mesure pas directement le décrochage scolaire. Un indicateur de contexte ne devient un score de risque qu’après définition, justification et validation d’une méthode dédiée.</div>', unsafe_allow_html=True)

elif page == "Explorer les territoires":
    st.markdown("#### Comparer les territoires")
    st.markdown('<div class="section-desc">Le classement ci-dessous porte uniquement sur l’indicateur et la période sélectionnés. Le sens favorable ou défavorable dépend de la nature de l’indicateur.</div>', unsafe_allow_html=True)
    periods_for_rank = sorted(view["periode"].unique(), key=period_key)
    chosen = st.selectbox("Période de comparaison", periods_for_rank, index=len(periods_for_rank)-1)
    rank = view[view["periode"] == chosen].groupby("region", as_index=False)["valeur"].mean().sort_values("valeur", ascending=False)
    a, b = st.columns([1.5, 1])
    with a:
        fig = px.bar(rank, x="valeur", y="region", orientation="h", text_auto=".2s")
        fig.update_traces(marker=dict(color=BLUE, cornerradius=5), textposition="outside", cliponaxis=False)
        fig.update_layout(height=max(400, len(rank)*28), margin=dict(l=5,r=50,t=10,b=10), paper_bgcolor="white", plot_bgcolor="white", font=dict(family="DM Sans",color=MUTED,size=11), xaxis_title=unit, yaxis_title="")
        fig.update_xaxes(gridcolor="#EDF1F5", zeroline=False)
        fig.update_yaxes(categoryorder="total ascending", showgrid=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    with b:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("**Repères de comparaison**")
        st.metric("Médiane territoriale", fmt(rank["valeur"].median(), unit))
        st.metric("Valeur maximale", fmt(rank["valeur"].max(), unit))
        st.metric("Valeur minimale", fmt(rank["valeur"].min(), unit))
        st.metric("Nombre de régions", len(rank))
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div class="note">Un niveau élevé n’est pas automatiquement un risque élevé : l’interprétation doit tenir compte de la définition de l’indicateur.</div>', unsafe_allow_html=True)
    st.dataframe(rank.rename(columns={"region":"Région","valeur":f"Valeur ({unit})"}), use_container_width=True, hide_index=True)

elif page == "Suivre les évolutions":
    st.markdown("#### Lire les trajectoires dans le temps")
    trend = view.groupby(["periode","region"], as_index=False)["valeur"].mean()
    ordered_periods = sorted(trend["periode"].unique(), key=period_key)
    trend["periode"] = pd.Categorical(trend["periode"], categories=ordered_periods, ordered=True)
    chosen_regions = st.multiselect("Régions à afficher", sorted(trend["region"].unique()), default=sorted(trend["region"].unique())[:5])
    trend = trend[trend["region"].isin(chosen_regions)]
    fig = px.line(trend.sort_values("periode"), x="periode", y="valeur", color="region", markers=True)
    fig.update_layout(height=480, margin=dict(l=10,r=10,t=25,b=10), paper_bgcolor="white", plot_bgcolor="white", font=dict(family="DM Sans",color=MUTED,size=11), xaxis_title="", yaxis_title=unit, legend_title="Région", hovermode="x unified")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#EDF1F5", zeroline=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="note">Les périodes sont ordonnées à partir de leur année de référence. Les années scolaires et les années civiles restent identifiées selon la source ; elles ne doivent pas être fusionnées sans harmonisation.</div>', unsafe_allow_html=True)

else:
    st.markdown("#### Transparence des données")
    c1, c2, c3 = st.columns(3)
    c1.metric("Observations dans la sélection", f"{len(view):,}".replace(",", " "))
    c2.metric("Régions", view["region"].nunique())
    c3.metric("Périodes", view["periode"].nunique())
    st.markdown("##### Contrôles automatiques")
    checks = [
        ("Valeurs manquantes", int(view["valeur"].isna().sum()), "success"),
        ("Valeurs négatives", int((view["valeur"] < 0).sum()), "warning"),
        ("Clés territoriales répétées", duplicate_rows, "error" if duplicate_rows else "success"),
    ]
    for label, number, status in checks:
        icon = "✓" if number == 0 else "!"
        st.markdown(f'<div class="metric-card" style="min-height:0;margin:7px 0;padding:12px 15px"><b style="color:{GREEN if number == 0 else RED}">{icon}</b> &nbsp;{label}<span style="float:right;font-weight:800">{number}</span></div>', unsafe_allow_html=True)
    st.write("")
    st.markdown("##### Ce que les données permettent — et ne permettent pas — de dire")
    st.markdown(
        """
        <div class="panel">
        <b style="color:#168A70">Ce que l'on peut décrire</b>
        <ul><li>Les niveaux des indicateurs scolaires présents dans le fichier.</li><li>Les écarts entre régions et les évolutions par période.</li><li>Les différences selon le sexe ou la modalité lorsqu'elles sont disponibles.</li></ul>
        <b style="color:#C18A2B">Ce qu'il ne faut pas conclure trop vite</b>
        <ul><li>Ces indicateurs ne sont pas des abandons observés.</li><li>Une baisse d'effectifs ne prouve pas un décrochage.</li><li>Aucun score prédictif ne doit être affiché avant définition d'une cible, validation temporelle et mesure de performance.</li></ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown("##### Aperçu des observations")
    st.dataframe(view.sort_values(["periode","region"], key=lambda s: s.map(lambda x: period_key(x)[0]) if s.name == "periode" else s), use_container_width=True, hide_index=True)

st.markdown(
    '<div class="footer">VIGIE ÉCOLE · Data Challenge Burkina 2026 · Défi 1 — Prototype analytique. Les données brutes restent locales. Les indicateurs présentés sont descriptifs et ne constituent pas, à eux seuls, une mesure du décrochage.</div>',
    unsafe_allow_html=True,
)
