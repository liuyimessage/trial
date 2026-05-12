"""Tab 6 — Idea Generation (AI Chatbot)."""
import streamlit as st
from utils.translations import t
from utils.ai_client import build_system_prompt, chat_completion

_STARTER_CHIPS_EN = [
    "What categories have no WAVE initiative?",
    "Suggest 3 new savings ideas for Construction spend ($42M)",
    "Which initiatives are below 50% of their business case?",
    "What is the highest-risk supplier concentration?",
    "Compare F&B WAVE initiatives vs Merchandise WAVE initiatives",
    "How can we reduce Spend w/o Justification in Clothing/Uniforms?",
]
_STARTER_CHIPS_JP = [
    "WAVEイニシアティブのないカテゴリは？",
    "建設支出（$42M）の新しい節約アイデアを3つ提案して",
    "ビジネスケースの50%未満のイニシアティブは？",
    "最も高リスクのサプライヤー集中度は？",
    "F&B vs Merchandiseのイニシアティブを比較して",
    "Clothing/Uniformsの正当理由なし支出を減らすには？",
]


def render(lang: str = "en"):
    st.title(f"💡 {t('tab_idea', lang)}")
    st.caption(t("idea_sub", lang))

    # ── Check API key ─────────────────────────────────────────────────────────
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    key_valid = api_key and api_key != "PASTE_YOUR_JWT_TOKEN_HERE"

    if not key_valid:
        st.warning(
            "⚠️ No API key found. Add your McKinsey JWT token to the `.env` file as `OPENAI_API_KEY` "
            "and restart the app." if lang == "en" else
            "⚠️ APIキーが見つかりません。`.env`ファイルに`OPENAI_API_KEY`としてMcKinsey JWTトークンを追加してください。"
        )

    # ── Starter chips ─────────────────────────────────────────────────────────
    chips = _STARTER_CHIPS_EN if lang == "en" else _STARTER_CHIPS_JP
    if not st.session_state.chat_history:
        st.markdown("**Starter questions:**" if lang == "en" else "**よくある質問:**")
        chip_cols = st.columns(3)
        for i, chip in enumerate(chips):
            if chip_cols[i % 3].button(chip, key=f"chip_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": chip})
                st.rerun()

    # ── Chat history display ──────────────────────────────────────────────────
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ── User input ────────────────────────────────────────────────────────────
    col_input, col_clear = st.columns([8, 1])
    with col_clear:
        if st.button(t("idea_clear", lang), use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    prompt = st.chat_input(t("idea_ph", lang))
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if not key_valid:
            error_msg = (
                "Cannot reach AI — no valid API key. Please add your McKinsey JWT token to `.env`."
                if lang == "en" else
                "APIキーが無効です。`.env`ファイルにMcKinsey JWTトークンを追加してください。"
            )
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            with st.chat_message("assistant"):
                st.error(error_msg)
        else:
            messages = [{"role": "system", "content": build_system_prompt()}]
            messages += st.session_state.chat_history

            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_response = ""
                try:
                    stream = chat_completion(messages, stream=True)
                    for chunk in stream:
                        delta = chunk.choices[0].delta.content or ""
                        full_response += delta
                        placeholder.markdown(full_response + "▌")
                    placeholder.markdown(full_response)
                except ValueError as ve:
                    err = str(ve)
                    placeholder.error(err)
                    full_response = f"Error: {err}"
                except Exception as exc:
                    err = f"Unexpected error: {exc}"
                    placeholder.error(err)
                    full_response = err

            st.session_state.chat_history.append(
                {"role": "assistant", "content": full_response}
            )
