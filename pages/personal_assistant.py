import io
import hashlib
import streamlit as st
import speech_recognition as sr

from utils.gemini_ai import GeminiAI
from utils.speaker import Speaker


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CodeBox AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PREMIUM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(37, 99, 235, 0.10), transparent 28%),
            radial-gradient(circle at 85% 15%, rgba(6, 182, 212, 0.08), transparent 25%),
            #070b12;
        color: #e8eef7;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #090e17 0%,
                #0b111c 55%,
                #080c13 100%
            );
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #8190a5;
    }

    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {
        width: 100%;
        min-height: 44px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.035);
        color: #e8eef7;
        font-weight: 650;
        transition:
            transform 0.18s ease,
            border-color 0.18s ease,
            background 0.18s ease,
            box-shadow 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: rgba(34,211,238,0.45);
        background: rgba(34,211,238,0.08);
        box-shadow: 0 8px 25px rgba(0,0,0,0.20);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* =========================
       TITLE
       ========================= */

    h1 {
        letter-spacing: -1.2px;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 850;
        line-height: 1.05;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        color: #8795a9;
        font-size: 1.05rem;
        margin-bottom: 1.8rem;
    }

    /* =========================
       CHAT
       ========================= */

    [data-testid="stChatMessage"] {
        border: 1px solid rgba(255,255,255,0.055);
        border-radius: 18px;
        padding: 0.7rem 0.9rem;
        margin-bottom: 0.75rem;
        background: rgba(255,255,255,0.018);
        transition:
            border-color 0.2s ease,
            background 0.2s ease,
            transform 0.2s ease;
    }

    [data-testid="stChatMessage"]:hover {
        border-color: rgba(34,211,238,0.16);
        background: rgba(255,255,255,0.028);
    }

    [data-testid="stChatInput"] {
        border-radius: 18px;
    }

    [data-testid="stChatInput"] textarea {
        background: #0d1420 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        color: #edf4ff !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: rgba(34,211,238,0.55) !important;
        box-shadow: 0 0 0 3px rgba(34,211,238,0.07) !important;
    }

    /* =========================
       EXPANDER
       ========================= */

    [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 16px !important;
        background: rgba(255,255,255,0.018);
        overflow: hidden;
    }

    [data-testid="stExpander"] summary {
        font-weight: 700;
    }

    /* =========================
       AUDIO
       ========================= */

    [data-testid="stAudioInput"] {
        border-radius: 14px;
    }

    audio {
        width: 100%;
        border-radius: 12px;
    }

    /* =========================
       ALERTS
       ========================= */

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    /* =========================
       DIVIDERS
       ========================= */

    hr {
        border-color: rgba(255,255,255,0.06) !important;
        margin: 1.3rem 0;
    }

    /* =========================
       SCROLLBAR
       ========================= */

    ::-webkit-scrollbar {
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #070b12;
    }

    ::-webkit-scrollbar-thumb {
        background: #1b2737;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #26364c;
    }

    /* =========================
       MOBILE
       ========================= */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero-title {
            font-size: 2.1rem;
        }

        .hero-subtitle {
            font-size: 0.95rem;
        }

    }

    /* =========================
       REDUCED MOTION
       ========================= */

    @media (prefers-reduced-motion: reduce) {

        *,
        *::before,
        *::after {
            transition: none !important;
            animation: none !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "assistant" not in st.session_state:
    st.session_state.assistant = None

if "speaker" not in st.session_state:
    st.session_state.speaker = None

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if "processed_audio_hash" not in st.session_state:
    st.session_state.processed_audio_hash = ""

if "is_processing" not in st.session_state:
    st.session_state.is_processing = False


# =========================================================
# INITIALIZE AI
# =========================================================

if st.session_state.assistant is None:
    try:
        st.session_state.assistant = GeminiAI()
    except Exception as e:
        st.error(f"تعذر تشغيل Gemini AI: {e}")

if st.session_state.speaker is None:
    try:
        st.session_state.speaker = Speaker()
    except Exception:
        st.session_state.speaker = None


assistant = st.session_state.assistant
speaker = st.session_state.speaker


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 CodeBox AI")
    st.caption("Personal AI Assistant")

    st.divider()

    if st.button("✨ محادثة جديدة", use_container_width=True):

        st.session_state.messages = []
        st.session_state.last_response = ""
        st.session_state.processed_audio_hash = ""

        if assistant is not None:
            try:
                assistant.reset_chat()
            except Exception:
                pass

        if speaker is not None:
            try:
                speaker.stop()
            except Exception:
                pass

        st.rerun()

    if st.button("⏹️ إيقاف الصوت", use_container_width=True):

        if speaker is not None:
            try:
                speaker.stop()
                st.toast("تم إيقاف الصوت")
            except Exception:
                st.warning("تعذر إيقاف الصوت.")

    st.divider()

    st.subheader("⚡ الإمكانيات")

    st.write("🐍 Python")
    st.write("💻 C++ / Java")
    st.write("🌐 Web Development")
    st.write("🗄️ SQL")
    st.write("🐞 Debugging")
    st.write("🤖 Artificial Intelligence")

    st.divider()

    if assistant is not None:
        st.success("AI متصل")


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<p class="hero-title">CodeBox AI 🤖</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="hero-subtitle">مساعدك الذكي للبرمجة والتكنولوجيا — اسأل، ناقش، واتكلم معاه بصوتك.</p>',
    unsafe_allow_html=True
)


# =========================================================
# QUICK ACTIONS
# =========================================================

if not st.session_state.messages:

    st.info(
        "👋 أهلاً بيك يا Mido! اكتب سؤالك تحت أو استخدم الميكروفون للتحدث مع المساعد."
    )

    st.write("### 🚀 جرّب تسألني")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("🐍 اشرحلي Python", use_container_width=True):
            st.session_state.quick_prompt = (
                "اشرحلي Python بطريقة بسيطة ومناسبة لمستواي مع مثال عملي."
            )
            st.rerun()

    with c2:
        if st.button("🐞 ساعدني في Bug", use_container_width=True):
            st.session_state.quick_prompt = (
                "ساعدني في اكتشاف أخطاء في كود Python واشرحلي طريقة التفكير في حلها."
            )
            st.rerun()

    with c3:
        if st.button("🤖 فكرة مشروع AI", use_container_width=True):
            st.session_state.quick_prompt = (
                "اقترحلي فكرة مشروع AI عملية ومميزة أقدر أطورها باستخدام Python."
            )
            st.rerun()


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    role = message.get("role", "assistant")
    content = message.get("content", "")

    if role == "user":
        avatar = "🧑‍💻"
    else:
        avatar = "🤖"

    with st.chat_message(role, avatar=avatar):
        st.markdown(content)


# =========================================================
# VOICE SECTION
# =========================================================

with st.expander("🎙️ التحدث مع CodeBox AI"):

    st.caption(
        "سجل رسالتك بالعربي أو الإنجليزي، وسيتم تحويلها إلى نص وإرسالها للمساعد."
    )

    audio_value = st.audio_input(
        "🎤 تسجيل رسالة",
        key="voice_recorder"
    )

    if audio_value is not None:

        audio_bytes = audio_value.getvalue()

        current_hash = hashlib.sha256(audio_bytes).hexdigest()

        if current_hash != st.session_state.processed_audio_hash:

            st.session_state.processed_audio_hash = current_hash

            recognizer = sr.Recognizer()

            try:

                audio_file = io.BytesIO(audio_bytes)

                with sr.AudioFile(audio_file) as source:
                    recorded_audio = recognizer.record(source)

                with st.spinner("🎧 بفهم كلامك..."):

                    voice_text = recognizer.recognize_google(
                        recorded_audio,
                        language="ar-EG"
                    )

                st.success(f"تم التعرف على الكلام: {voice_text}")

                st.session_state.voice_prompt = voice_text

                st.rerun()

            except sr.UnknownValueError:

                st.warning(
                    "مش قادر أفهم التسجيل. حاول تسجل بصوت أوضح."
                )

            except sr.RequestError:

                st.error(
                    "حصلت مشكلة في خدمة التعرف على الصوت."
                )

            except Exception as e:

                st.error(
                    f"حصل خطأ أثناء معالجة الصوت: {e}"
                )


# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "اكتب رسالتك هنا... 💬"
)


# =========================================================
# QUICK PROMPT
# =========================================================

if "quick_prompt" in st.session_state:

    prompt = st.session_state.quick_prompt

    del st.session_state.quick_prompt


# =========================================================
# VOICE PROMPT
# =========================================================

if "voice_prompt" in st.session_state:

    prompt = st.session_state.voice_prompt

    del st.session_state.voice_prompt


# =========================================================
# PROCESS MESSAGE
# =========================================================

if prompt:

    prompt = prompt.strip()

    if prompt:

        # -----------------------------
        # USER MESSAGE
        # -----------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # -----------------------------
        # AI RESPONSE
        # -----------------------------

        with st.chat_message("assistant", avatar="🤖"):

            if assistant is None:

                response = (
                    "❌ المساعد غير متصل حاليًا. "
                    "تأكد من إعداد Gemini API."
                )

                st.error(response)

            else:

                try:

                    with st.spinner("🤖 CodeBox AI بيفكر..."):

                        response = assistant.generate_response(
                            prompt
                        )

                    if not response:
                        response = "مش لاقي رد مناسب دلوقتي. جرّب السؤال مرة تانية."

                    st.markdown(response)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response
                        }
                    )

                    st.session_state.last_response = response

                    # -----------------------------
                    # VOICE RESPONSE
                    # -----------------------------

                    if speaker is not None:

                        try:
                            speaker.speak(response)
                        except Exception:
                            pass

                except Exception as e:

                    response = (
                        "حصل خطأ أثناء التواصل مع Gemini.\n\n"
                        f"`{e}`"
                    )

                    st.error(response)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response
                        }
                    )


# =========================================================
# RESPONSE CONTROLS
# =========================================================

if st.session_state.last_response:

    st.divider()

    st.caption("🔊 التحكم في الرد الصوتي")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "▶️ تشغيل الرد مرة أخرى",
            use_container_width=True
        ):

            if speaker is not None:

                try:
                    speaker.speak(
                        st.session_state.last_response
                    )
                except Exception as e:
                    st.error(f"تعذر تشغيل الصوت: {e}")

    with col2:

        if st.button(
            "⏹️ إيقاف الرد",
            use_container_width=True
        ):

            if speaker is not None:

                try:
                    speaker.stop()
                except Exception:
                    pass


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "CodeBox AI • Built with Python + Streamlit + Gemini"
)
