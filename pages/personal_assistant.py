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


/* =========================
   PREMIUM AI BUTTONS
   ========================= */

.stButton {
    transition: all 0.25s ease;
}

.stButton > button {
    position: relative;
    width: 100%;
    min-height: 48px;

    border-radius: 14px;

    border: 1px solid rgba(56, 189, 248, 0.18);

    background:
        linear-gradient(
            135deg,
            rgba(15, 23, 42, 0.95),
            rgba(17, 24, 39, 0.95)
        );

    color: #eaf6ff;

    font-size: 0.95rem;
    font-weight: 700;

    letter-spacing: 0.1px;

    box-shadow:
        0 4px 15px rgba(0, 0, 0, 0.18),
        inset 0 1px 0 rgba(255,255,255,0.04);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        border-color 0.2s ease,
        background 0.2s ease;
}


/* Hover */

.stButton > button:hover {

    transform: translateY(-3px);

    border-color: rgba(34, 211, 238, 0.65);

    background:
        linear-gradient(
            135deg,
            rgba(14, 165, 233, 0.16),
            rgba(37, 99, 235, 0.18)
        );

    box-shadow:
        0 10px 30px rgba(14, 165, 233, 0.18),
        0 0 18px rgba(34, 211, 238, 0.10);

    color: #ffffff;
}


/* Click */

.stButton > button:active {

    transform: scale(0.97);

    box-shadow:
        0 3px 12px rgba(14, 165, 233, 0.15);
}


/* Focus */

.stButton > button:focus {

    border-color: rgba(34, 211, 238, 0.7) !important;

    box-shadow:
        0 0 0 3px rgba(34, 211, 238, 0.08),
        0 0 20px rgba(34, 211, 238, 0.10) !important;
}


/* =========================
   SIDEBAR BUTTONS
   ========================= */

section[data-testid="stSidebar"] .stButton > button {

    min-height: 46px;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.025),
            rgba(255,255,255,0.045)
        );

    border: 1px solid rgba(255,255,255,0.07);

    text-align: left;

    padding-left: 16px;
}


section[data-testid="stSidebar"] .stButton > button:hover {

    background:
        linear-gradient(
            135deg,
            rgba(37,99,235,0.20),
            rgba(6,182,212,0.12)
        );

    border-color: rgba(34,211,238,0.45);

    box-shadow:
        0 8px 25px rgba(0,0,0,0.25);
}


/* =========================
   QUICK ACTION BUTTONS
   ========================= */

div[data-testid="stHorizontalBlock"] .stButton > button {

    min-height: 58px;

    border-radius: 16px;

    font-size: 1rem;

    background:
        linear-gradient(
            145deg,
            rgba(15,23,42,0.95),
            rgba(15,30,45,0.95)
        );

    border: 1px solid rgba(56,189,248,0.12);
}


div[data-testid="stHorizontalBlock"] .stButton > button:hover {

    transform: translateY(-5px) scale(1.01);

    border-color: rgba(34,211,238,0.55);

    box-shadow:
        0 15px 35px rgba(14,165,233,0.16),
        0 0 25px rgba(34,211,238,0.08);
}
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
