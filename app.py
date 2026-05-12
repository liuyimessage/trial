"""
UDX Spend Analytics — V9 Streamlit Dashboard
Entry point: run with `streamlit run app.py`
"""
import streamlit as st

st.set_page_config(
    page_title="UDX Spend Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS — McKinsey dark theme ─────────────────────────────────────────
st.markdown("""
<style>
/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── App background ── */
.stApp { background-color: #0f1117; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0a0e1a !important;
    border-right: 1px solid #1e2642;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }

/* ── Sidebar nav radio — style as tab buttons ── */
[data-testid="stSidebar"] .stRadio > div {
    gap: 3px;
}
[data-testid="stSidebar"] .stRadio label {
    background: #131929;
    border: 1px solid #1e2642;
    border-radius: 8px;
    padding: 8px 14px !important;
    margin: 1px 0;
    cursor: pointer;
    color: #a8b8d0 !important;
    font-size: 13px !important;
    transition: background 0.15s, border-color 0.15s;
    display: block;
    width: 100%;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: #1a2240 !important;
    border-color: #4f8ef7 !important;
    color: #e8eaf0 !important;
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] > div:first-child {
    display: none;
}

/* ── Language toggle buttons ── */
[data-testid="stSidebar"] .stButton button {
    border-radius: 6px;
    font-size: 12px;
    padding: 4px 8px;
}

/* ── Main content padding ── */
.main .block-container {
    padding-top: 1.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 1400px;
}

/* ── Page titles ── */
h1 {
    color: #4f8ef7 !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.1rem !important;
    letter-spacing: -0.3px;
}
h2 {
    color: #c8d0e0 !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}
h3 {
    color: #8090b0 !important;
    font-size: 0.95rem !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #131929 !important;
    border: 1px solid #1e2642 !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
}
[data-testid="stMetricLabel"] > div {
    color: #8090b0 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="stMetricValue"] > div {
    color: #e8eaf0 !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] > div { font-size: 12px !important; }

/* ── Dataframes / tables ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1e2642;
    border-radius: 8px;
    overflow: hidden;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: #131929;
    border: 1px solid #1e2642 !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary {
    color: #c8d0e0 !important;
    font-weight: 600;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #131929 !important;
    border: 1px solid #1e2642 !important;
    border-radius: 10px !important;
    margin: 4px 0 !important;
    padding: 10px 14px !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {
    background: #131929 !important;
    border: 1px solid #2a3560 !important;
    border-radius: 8px !important;
    color: #e8eaf0 !important;
}

/* ── Buttons (starter chips) ── */
.stButton button {
    background: #131929 !important;
    border: 1px solid #2a3560 !important;
    color: #a8b8d0 !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    transition: all 0.15s;
}
.stButton button:hover {
    background: #1a2a5e !important;
    border-color: #4f8ef7 !important;
    color: #e8eaf0 !important;
}
.stButton button[kind="primary"] {
    background: #4f8ef7 !important;
    border-color: #4f8ef7 !important;
    color: #fff !important;
}

/* ── Divider ── */
hr { border-color: #1e2642 !important; }

/* ── Captions / small text ── */
[data-testid="stCaptionContainer"] { color: #606880 !important; }

/* ── Select / dropdown ── */
[data-testid="stSelectbox"] select,
[data-baseweb="select"] {
    background: #131929 !important;
    border-color: #2a3560 !important;
    color: #e8eaf0 !important;
}

/* ── Tabs (if used inside pages) ── */
[data-testid="stTabs"] [role="tab"] {
    background: #131929;
    border: 1px solid #1e2642;
    border-radius: 6px 6px 0 0;
    color: #8090b0;
    font-size: 13px;
    padding: 6px 16px;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #1a2a5e;
    border-color: #4f8ef7;
    color: #4f8ef7;
}

/* ── Warning / info boxes ── */
[data-testid="stAlert"] {
    border-radius: 8px;
    border-left: 4px solid;
}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "bc_cases" not in st.session_state:
    st.session_state.bc_cases = []

# ── Imports after set_page_config ────────────────────────────────────────────
from utils.translations import t

lang = st.session_state.lang

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / title
    st.markdown(
        f"<h2 style='color:#4f8ef7;margin-bottom:0'>📊 UDX</h2>"
        f"<p style='color:#888;font-size:12px;margin-top:2px'>{t('app_subtitle', lang)}</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Language toggle
    col_en, col_jp = st.columns(2)
    with col_en:
        if st.button("EN", use_container_width=True,
                     type="primary" if lang == "en" else "secondary"):
            st.session_state.lang = "en"
            st.rerun()
    with col_jp:
        if st.button("日本語", use_container_width=True,
                     type="primary" if lang == "jp" else "secondary"):
            st.session_state.lang = "jp"
            st.rerun()

    st.divider()

    # Navigation
    page = st.radio(
        "Navigation",
        options=[
            "spend_pulse",
            "cat_intel",
            "supplier_intel",
            "proc_behavior",
            "savings_map",
            "idea_gen",
            "biz_case",
            "data_req",
            "assumptions",
        ],
        format_func=lambda x: {
            "spend_pulse":    f"📈 {t('tab_pulse', lang)}",
            "cat_intel":      f"🗂️ {t('tab_cat', lang)}",
            "supplier_intel": f"🏭 {t('tab_supplier', lang)}",
            "proc_behavior":  f"⚙️ {t('tab_behavior', lang)}",
            "savings_map":    f"💰 {t('tab_savings', lang)}",
            "idea_gen":       f"💡 {t('tab_idea', lang)}",
            "biz_case":       f"📋 {t('tab_bc', lang)}",
            "data_req":       f"📂 {t('tab_datareq', lang)}",
            "assumptions":    f"📝 {t('tab_assumptions', lang)}",
        }[x],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("🔒 Draft for Review · Internal only")

# ── Page routing ──────────────────────────────────────────────────────────────
if page == "spend_pulse":
    import pages.spend_pulse as pg
elif page == "cat_intel":
    import pages.cat_intel as pg
elif page == "supplier_intel":
    import pages.supplier_intel as pg
elif page == "proc_behavior":
    import pages.proc_behavior as pg
elif page == "savings_map":
    import pages.savings_map as pg
elif page == "idea_gen":
    import pages.idea_gen as pg
elif page == "biz_case":
    import pages.biz_case as pg
elif page == "data_req":
    import pages.data_req as pg
else:
    import pages.assumptions as pg

pg.render(lang)
