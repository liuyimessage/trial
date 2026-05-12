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
