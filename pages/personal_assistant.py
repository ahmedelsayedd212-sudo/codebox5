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

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 5%,
                rgba(37, 99, 235, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(6, 182, 212, 0.09),
                transparent 25%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(59, 130, 246, 0.05),
                transparent 35%
            ),
            #060a11;

        color: #eaf2ff;
    }


    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }


    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #080d16 0%,
                #0a101b 50%,
                #070b12 100%
            );

        border-right: 1px solid rgba(255,255,255,0.055);
    }


    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.4rem;
    }


    section[data-testid="stSidebar"] h1 {

        font-size: 1.5rem;
        font-weight: 850;

        letter-spacing: -0.7px;
    }


    section[data-testid="stSidebar"] .stCaption {
        color: #7f8da1;
    }


    /* =====================================================
       PREMIUM BUTTON SYSTEM
       ===================================================== */

    .stButton {
        transition: all 0.25s ease;
    }


    .stButton > button {

        position: relative;

        width: 100%;
        min-height: 48px;

        border-radius: 14px;

        border: 1px solid rgba(56,189,248,0.16);

        background:
            linear-gradient(
                135deg,
                rgba(15,23,42,0.96),
                rgba(17,24,39,0.96)
            );

        color: #eaf6ff;

        font-size: 0.94rem;
        font-weight: 700;

        letter-spacing: 0.1px;

        box-shadow:
            0 5px 18px rgba(0,0,0,0.18),
            inset 0 1px 0 rgba(255,255,255,0.035);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease,
            background 0.2s ease;
    }


    .stButton > button:hover {

        transform: translateY(-3px);

        border-color: rgba(34,211,238,0.65);

        background:
            linear-gradient(
                135deg,
                rgba(14,165,233,0.15),
                rgba(37,99,235,0.18)
            );

        box-shadow:
            0 12px 30px rgba(14,165,233,0.18),
            0 0 20px rgba(34,211,238,0.09);

        color: #ffffff;
    }


    .stButton > button:active {
        transform: scale(0.97);
    }


    .stButton > button:focus {

        border-color: rgba(34,211,238,0.7) !important;

        box-shadow:
            0 0 0 3px rgba(34,211,238,0.07),
            0 0 20px rgba(34,211,238,0.10) !important;
    }


    /* =====================================================
       SIDEBAR BUTTONS
       ===================================================== */

    section[data-testid="stSidebar"] .stButton > button {

        min-height: 47px;

        text-align: left;

        padding-left: 16px;

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.025),
                rgba(255,255,255,0.045)
            );

        border: 1px solid rgba(255,255,255,0.065);
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
            0 9px 25px rgba(0,0,0,0.25);
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero-title {

        font-size: 3.1rem;

        font-weight: 900;

        line-height: 1.05;

        letter-spacing: -1.7px;

        margin-bottom: 0.35rem;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #b8eaff,
                #67e8f9
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .hero-subtitle {

        color: #8795a9;

        font-size: 1.05rem;

        margin-bottom: 1.7rem;
    }


    /* =====================================================
       CHAT
       ===================================================== */

    [data-testid="stChatMessage"] {

        border:
            1px solid rgba(255,255,255,0.055);

        border-radius: 18px;

        padding: 0.75rem 0.95rem;

        margin-bottom: 0.8rem;

        background:
            rgba(255,255,255,0.018);

        transition:
            border-color 0.2s ease,
            background 0.2s ease,
            transform 0.2s ease;
    }


    [data-testid="stChatMessage"]:hover {

        border-color:
            rgba(34,211,238,0.18);

        background:
            rgba(255,255,255,0.027);

        transform: translateY(-1px);
    }


    /* =====================================================
       CHAT INPUT
       ===================================================== */

    [data-testid="stChatInput"] {

        border-radius: 18px;
    }


    [data-testid="stChatInput"] textarea {

        background: #0c131f !important;

        border:
            1px solid rgba(255,255,255,0.08) !important;

        border-radius: 16px !important;

        color: #edf6ff !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }


    [data-testid="stChatInput"] textarea:focus {

        border-color:
            rgba(34,211,238,0.55) !important;

        box-shadow:
            0 0 0 3px rgba(34,211,238,0.06) !important;
    }


    /* =====================================================
       QUICK ACTION BUTTONS
       ===================================================== */

    div[data-testid="stHorizontalBlock"]
    .stButton > button {

        min-height: 62px;

        border-radius: 17px;

        font-size: 0.98rem;

        background:
            linear-gradient(
                145deg,
                rgba(11,20,35,0.97),
                rgba(15,30,45,0.96)
            );

        border:
            1px solid rgba(56,189,248,0.13);
    }


    div[data-testid="stHorizontalBlock"]
    .stButton > button:hover {

        transform:
            translateY(-5px) scale(1.015);

        border-color:
            rgba(34,211,238,0.58);

        box-shadow:
            0 15px 35px rgba(14,165,233,0.15),
            0 0 25px rgba(34,211,238,0.08);
    }


    /* =====================================================
       EXPANDER
       ===================================================== */

    [data-testid="stExpander"] {

        border:
            1px solid rgba(255,255,255,0.065) !important;

        border-radius: 16px !important;

        background:
            rgba(255,255,255,0.018);

        overflow: hidden;
    }


    [data-testid="stExpander"] summary {

        font-weight: 700;
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    [data-testid="stAlert"] {

        border-radius: 15px;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {

        border-color:
            rgba(255,255,255,0.055) !important;

        margin:
            1.3rem 0;
    }


    /* =====================================================
       SCROLLBAR
       ===================================================== */

    ::-webkit-scrollbar {
        width: 7px;
    }


    ::-webkit-scrollbar-track {
        background: #060a11;
    }


    ::-webkit-scrollbar-thumb {

        background: #1a2738;

        border-radius: 10px;
    }


    ::-webkit-scrollbar-thumb:hover {
        background: #26384f;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 700px) {

        .block-container {

            padding-left: 1rem;
            padding-right: 1rem;
        }


        .hero-title {
            font-size: 2.2rem;
        }


        .hero-subtitle {
            font-size: 0.94rem;
        }

    }


    /* =====================================================
       REDUCED MOTION
       ===================================================== */

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
    unsafe_allow_html=True
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


# =========================================================
# INITIALIZE GEMINI
# =========================================================

if st.session_state.assistant is None:

    try:

        st.session_state.assistant = GeminiAI()

    except Exception as e:

        st.error(
            f"تعذر تشغيل Gemini AI: {e}"
        )


# =========================================================
# INITIALIZE SPEAKER
# =========================================================

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

    st.caption(
        "Your personal AI coding assistant"
    )

    st.divider()


    if st.button(
        "✨  محادثة جديدة",
        use_container_width=True
    ):

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


    if st.button(
        "⏹️  إيقاف الصوت",
        use_container_width=True
    ):

        if speaker is not None:

            try:

                speaker.stop()

                st.toast(
                    "تم إيقاف الصوت 🔇"
                )

            except Exception:

                st.warning(
                    "تعذر إيقاف الصوت."
                )


    st.divider()


    st.subheader("⚡ قدرات CodeBox")


    st.caption("🐍  Python")

    st.caption("💻  C++ / Java")

    st.caption("🌐  HTML / CSS / JavaScript")

    st.caption("🗄️  SQL")

    st.caption("🐞  Debugging")

    st.caption("🤖  Artificial Intelligence")


    st.divider()


    if assistant is not None:

        st.success(
            "● AI Online"
        )

    else:

        st.error(
            "● AI Offline"
        )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<p class="hero-title">CodeBox AI 🤖</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="hero-subtitle">'
    'مساعدك الذكي للبرمجة والتكنولوجيا — اسأل، ناقش، واتكلم معاه بصوتك.'
    '</p>',
    unsafe_allow_html=True
)


# =========================================================
# EMPTY CHAT / QUICK ACTIONS
# =========================================================

if not st.session_state.messages:

    st.info(
        "👋 أهلاً بيك يا Mido! "
        "اكتب سؤالك تحت أو استخدم الميكروفون للتحدث مع CodeBox AI."
    )


    st.write("### 🚀 ابدأ بسرعة")


    col1, col2, col3 = st.columns(3)


    with col1:

        if st.button(
            "🐍  اشرحلي Python",
            use_container_width=True
        ):

            st.session_state.quick_prompt = (
                "اشرحلي Python بطريقة بسيطة ومناسبة لمستواي، "
                "مع أمثلة عملية."
            )

            st.rerun()


    with col2:

        if st.button(
            "🐞  ساعدني في Bug",
            use_container_width=True
        ):

            st.session_state.quick_prompt = (
                "ساعدني في اكتشاف وحل أخطاء Python، "
                "واشرحلي طريقة التفكير في حل الـ Bug."
            )

            st.rerun()


    with col3:

        if st.button(
            "🤖  فكرة مشروع AI",
            use_container_width=True
        ):

            st.session_state.quick_prompt = (
                "اقترحلي فكرة مشروع AI عملية ومميزة "
                "أقدر أطورها باستخدام Python."
            )

            st.rerun()


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    role = message["role"]

    content = message["content"]


    if role == "user":

        avatar = "🧑‍💻"

    else:

        avatar = "🤖"


    with st.chat_message(
        role,
        avatar=avatar
    ):

        st.markdown(content)


# =========================================================
# VOICE INPUT
# =========================================================

with st.expander(
    "🎙️  التحدث مع CodeBox AI"
):

    st.caption(
        "سجل رسالتك، وسيتم تحويل صوتك إلى نص وإرساله للمساعد."
    )


    audio_value = st.audio_input(
        "🎤 تسجيل رسالة",
        key="voice_recorder"
    )


    if audio_value is not None:

        audio_bytes = audio_value.getvalue()


        current_hash = hashlib.sha256(
            audio_bytes
        ).hexdigest()


        if (
            current_hash
            != st.session_state.processed_audio_hash
        ):

            st.session_state.processed_audio_hash = (
                current_hash
            )


            recognizer = sr.Recognizer()


            try:

                audio_file = io.BytesIO(
                    audio_bytes
                )


                with sr.AudioFile(
                    audio_file
                ) as source:

                    recorded_audio = (
                        recognizer.record(source)
                    )


                with st.spinner(
                    "🎧 بفهم كلامك..."
                ):

                    voice_text = (
                        recognizer.recognize_google(
                            recorded_audio,
                            language="ar-EG"
                        )
                    )


                st.success(
                    f"تم التعرف على كلامك: {voice_text}"
                )


                st.session_state.voice_prompt = (
                    voice_text
                )


                st.rerun()


            except sr.UnknownValueError:

                st.warning(
                    "مش قادر أفهم التسجيل. "
                    "حاول تسجل بصوت أوضح."
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
    "اكتب رسالتك إلى CodeBox AI... 💬"
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
# SEND MESSAGE
# =========================================================

if prompt:

    prompt = prompt.strip()


    if prompt:

        # =================================================
        # USER MESSAGE
        # =================================================

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )


        with st.chat_message(
            "user",
            avatar="🧑‍💻"
        ):

            st.markdown(prompt)


        # =================================================
        # AI RESPONSE
        # =================================================

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            if assistant is None:

                response = (
                    "❌ Gemini AI غير متصل حاليًا."
                )

                st.error(response)


            else:

                try:

                    with st.spinner(
                        "🤖 CodeBox AI بيفكر..."
                    ):

                        response = (
                            assistant.generate_response(
                                prompt
                            )
                        )


                    if not response:

                        response = (
                            "مش لاقي رد مناسب دلوقتي. "
                            "جرّب السؤال مرة تانية."
                        )


                    st.markdown(
                        response
                    )


                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response
                        }
                    )


                    st.session_state.last_response = (
                        response
                    )


                    # =====================================
                    # AUTO VOICE
                    # =====================================

                    if speaker is not None:

                        try:

                            speaker.speak(
                                response
                            )

                        except Exception:

                            pass


                except Exception as e:

                    response = (
                        "❌ حصل خطأ أثناء التواصل مع Gemini.\n\n"
                        f"`{e}`"
                    )


                    st.error(
                        response
                    )


                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response
                        }
                    )


# =========================================================
# AUDIO CONTROLS
# =========================================================

if st.session_state.last_response:

    st.divider()


    st.write("### 🔊 التحكم في الصوت")


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "▶️  تشغيل آخر رد",
            use_container_width=True
        ):

            if speaker is not None:

                try:

                    speaker.speak(
                        st.session_state.last_response
                    )

                except Exception as e:

                    st.error(
                        f"تعذر تشغيل الصوت: {e}"
                    )


    with col2:

        if st.button(
            "⏹️  إيقاف الرد",
            use_container_width=True
        ):

            if speaker is not None:

                try:

                    speaker.stop()

                    st.toast(
                        "تم إيقاف الصوت 🔇"
                    )

                except Exception:

                    pass


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "CodeBox AI  •  Python + Streamlit + Gemini"
)
