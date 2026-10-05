import io
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
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "assistant" not in st.session_state:
    st.session_state.assistant = None

if "speaker" not in st.session_state:
    st.session_state.speaker = None


# =========================================================
# PROFESSIONAL CSS
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
                circle at 50% -10%,
                rgba(14, 165, 233, 0.13),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 30%,
                rgba(37, 99, 235, 0.08),
                transparent 25%
            ),
            #070b12;

        color: #e5edf7;
    }


    .block-container {
        max-width: 1150px;
        padding-top: 1.2rem;
        padding-bottom: 7rem;
    }


    /* =====================================================
       REMOVE DEFAULT STREAMLIT ELEMENTS
       ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #090e17 0%,
                #070b12 100%
            );

        border-right: 1px solid rgba(255,255,255,0.06);
    }


    section[data-testid="stSidebar"] > div {
        padding-top: 1.2rem;
    }


    /* =====================================================
       BRAND
       ===================================================== */

    .brand-wrapper {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 4px;
    }


    .brand-icon {

        width: 44px;
        height: 44px;

        border-radius: 14px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 22px;

        background:
            linear-gradient(
                135deg,
                #0ea5e9,
                #2563eb
            );

        box-shadow:
            0 0 25px rgba(14,165,233,0.28);
    }


    .brand-name {

        font-size: 24px;
        font-weight: 800;
        color: #f8fafc;
    }


    .brand-name span {
        color: #38bdf8;
    }


    .brand-description {

        color: #64748b;
        font-size: 11px;
        margin-left: 56px;
        margin-top: -5px;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero {

        text-align: center;

        padding:
            42px
            20px
            25px;
    }


    .ai-logo {

        width: 88px;
        height: 88px;

        margin: auto;
        margin-bottom: 22px;

        border-radius: 27px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 42px;

        background:
            linear-gradient(
                135deg,
                #0ea5e9,
                #2563eb 60%,
                #1d4ed8
            );

        box-shadow:
            0 0 35px rgba(14,165,233,0.25),
            inset 0 1px 1px rgba(255,255,255,0.2);
    }


    .hero-title {

        font-size: 38px;
        font-weight: 850;

        letter-spacing: -1.2px;

        color: #f8fafc;

        margin-bottom: 8px;
    }


    .hero-subtitle {

        max-width: 600px;

        margin: auto;

        color: #7c8ba1;

        font-size: 15px;

        line-height: 1.7;
    }


    /* =====================================================
       STATUS
       ===================================================== */

    .online-status {

        display: inline-flex;

        align-items: center;

        gap: 7px;

        margin-top: 18px;

        padding:
            7px
            13px;

        border-radius: 30px;

        background: rgba(34,197,94,0.07);

        border: 1px solid rgba(34,197,94,0.15);

        color: #86efac;

        font-size: 11px;

        font-weight: 700;

        letter-spacing: .4px;
    }


    .online-dot {

        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #22c55e;

        box-shadow:
            0 0 10px #22c55e;
    }


    /* =====================================================
       FEATURE PILLS
       ===================================================== */

    .features {

        display: flex;

        justify-content: center;

        flex-wrap: wrap;

        gap: 8px;

        margin:
            10px
            auto
            35px;
    }


    .feature {

        padding:
            7px
            12px;

        border-radius: 9px;

        background: rgba(255,255,255,0.025);

        border:
            1px solid
            rgba(255,255,255,0.06);

        color: #94a3b8;

        font-size: 11px;
    }


    /* =====================================================
       CHAT AREA
       ===================================================== */

    [data-testid="stChatMessage"] {

        border-radius: 17px;

        border:
            1px solid
            rgba(255,255,255,0.055);

        background:
            rgba(255,255,255,0.018);

        margin-bottom: 12px;

        padding: 8px 14px;

        transition:
            border-color .2s ease,
            background .2s ease;
    }


    [data-testid="stChatMessage"]:hover {

        border-color:
            rgba(56,189,248,0.15);

        background:
            rgba(255,255,255,0.025);
    }


    /* =====================================================
       CHAT INPUT
       ===================================================== */

    [data-testid="stChatInput"] {

        position: fixed;

        bottom: 20px;

        left: 50%;

        transform: translateX(-50%);

        width: min(820px, 72vw);

        z-index: 1000;
    }


    [data-testid="stChatInput"] > div {

        background: #101722 !important;

        border:
            1px solid
            #263244 !important;

        border-radius: 18px !important;

        box-shadow:
            0 12px 45px rgba(0,0,0,0.45),
            0 0 25px rgba(14,165,233,0.04);
    }


    [data-testid="stChatInput"] textarea {

        color: #f8fafc !important;

        font-size: 14px !important;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {

        width: 100%;

        min-height: 43px;

        border-radius: 12px !important;

        background:
            #101722 !important;

        color: #cbd5e1 !important;

        border:
            1px solid
            #263244 !important;

        font-weight: 650;

        transition:
            all .2s ease;
    }


    .stButton > button:hover {

        color: #ffffff !important;

        border-color:
            #0ea5e9 !important;

        background:
            #131e2d !important;

        box-shadow:
            0 0 18px
            rgba(14,165,233,0.08);
    }


    /* =====================================================
       EXPANDER
       ===================================================== */

    [data-testid="stExpander"] {

        background:
            rgba(255,255,255,0.018);

        border:
            1px solid
            rgba(255,255,255,0.06);

        border-radius: 14px;
    }


    /* =====================================================
       AUDIO
       ===================================================== */

    [data-testid="stAudioInput"] {

        border-radius: 14px;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {

        border: none !important;

        border-top:
            1px solid
            rgba(255,255,255,0.055) !important;

        margin:
            25px
            0 !important;
    }


    /* =====================================================
       SIDEBAR SECTION
       ===================================================== */

    .side-label {

        color: #475569;

        font-size: 10px;

        text-transform: uppercase;

        letter-spacing: 1.4px;

        margin:
            18px
            0
            9px;
    }


    .side-item {

        padding:
            10px
            12px;

        border-radius: 10px;

        margin-bottom: 5px;

        color: #94a3b8;

        font-size: 12px;

        background:
            rgba(255,255,255,0.018);

        border:
            1px solid
            rgba(255,255,255,0.035);
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {

        text-align: center;

        color: #334155;

        font-size: 10px;

        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# INITIALIZE AI
# =========================================================

if st.session_state.assistant is None:

    try:

        st.session_state.assistant = GeminiAI()

    except Exception as e:

        st.error(
            f"حدث خطأ أثناء تشغيل Gemini AI:\n\n{e}"
        )

        st.stop()


# =========================================================
# INITIALIZE SPEAKER
# =========================================================

if st.session_state.speaker is None:

    try:

        st.session_state.speaker = Speaker()

    except Exception:

        st.session_state.speaker = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-wrapper">

            <div class="brand-icon">
                🤖
            </div>

            <div class="brand-name">
                Code<span>Box</span>
            </div>

        </div>

        <div class="brand-description">
            Personal AI Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.divider()


    st.markdown(
        '<div class="side-label">WORKSPACE</div>',
        unsafe_allow_html=True,
    )


    if st.button(
        "＋  محادثة جديدة",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.session_state.last_response = None

        try:

            st.session_state.assistant.reset_chat()

        except Exception:

            pass


        if st.session_state.speaker:

            try:

                st.session_state.speaker.stop()

            except Exception:

                pass


        st.rerun()


    if st.button(
        "◼  إيقاف الصوت",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            try:

                st.session_state.speaker.stop()

            except Exception:

                pass


    st.markdown(
        '<div class="side-label">CAPABILITIES</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="side-item">🐍 Python & Programming</div>
        <div class="side-item">🤖 Artificial Intelligence</div>
        <div class="side-item">🐞 Debugging</div>
        <div class="side-item">🎤 Voice Input</div>
        <div class="side-item">🔊 Voice Response</div>
        """,
        unsafe_allow_html=True,
    )


    st.divider()


    st.caption(
        "CodeBox AI • Gemini"
    )


# =========================================================
# HERO WHEN CHAT IS EMPTY
# =========================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="hero">

            <div class="ai-logo">
                ✦
            </div>

            <div class="hero-title">
                CodeBox AI
            </div>

            <div class="hero-subtitle">
                مساعدك الشخصي الذكي للبرمجة والتكنولوجيا.
                اكتب سؤالك وابدأ محادثة جديدة.
            </div>

            <div class="online-status">
                <span class="online-dot"></span>
                AI SYSTEM ONLINE
            </div>

        </div>


        <div class="features">

            <div class="feature">
                🐍 Python
            </div>

            <div class="feature">
                💻 Programming
            </div>

            <div class="feature">
                🤖 AI
            </div>

            <div class="feature">
                🐞 Debugging
            </div>

            <div class="feature">
                🎤 Voice
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "اكتب رسالتك إلى CodeBox AI..."
)


# =========================================================
# VOICE INPUT
# =========================================================

with st.expander(
    "🎙️  التحدث مع المساعد"
):

    st.caption(
        "سجل رسالتك وسيتم تحويلها إلى نص."
    )

    audio_value = st.audio_input(
        "تسجيل رسالة"
    )

    voice_text = None


    if audio_value is not None:

        try:

            recognizer = sr.Recognizer()

            audio_bytes = (
                audio_value.getvalue()
            )

            audio_file = io.BytesIO(
                audio_bytes
            )


            with st.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)


            with st.spinner(
                "جاري تحويل الصوت..."
            ):

                voice_text = (
                    recognizer.recognize_google(
                        audio_data,
                        language="ar-EG"
                    )
                )


            st.success(
                f"تم التعرف على: {voice_text}"
            )


        except sr.UnknownValueError:

            st.error(
                "لم أتمكن من فهم التسجيل."
            )


        except sr.RequestError:

            st.error(
                "خدمة تحويل الصوت غير متاحة."
            )


        except Exception as e:

            st.error(
                f"حدث خطأ:\n{e}"
            )


# =========================================================
# SELECT MESSAGE
# =========================================================

user_message = None


if voice_text:

    user_message = voice_text

elif prompt:

    user_message = prompt


# =========================================================
# SEND MESSAGE
# =========================================================

if user_message:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )


    with st.chat_message("user"):

        st.markdown(
            user_message
        )


    with st.chat_message("assistant"):

        with st.spinner(
            "CodeBox AI يفكر..."
        ):

            try:

                response = (
                    st.session_state.assistant
                    .generate_response(
                        user_message
                    )
                )


                st.markdown(
                    response
                )


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )


                st.session_state.last_response = response


                if st.session_state.speaker:

                    try:

                        st.session_state.speaker.speak(
                            response
                        )

                    except Exception as e:

                        st.warning(
                            f"تعذر تشغيل الصوت: {e}"
                        )


            except Exception as e:

                error_message = (
                    "حدث خطأ أثناء التواصل مع Gemini:\n\n"
                    f"{e}"
                )


                st.error(
                    error_message
                )


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )


# =========================================================
# AUDIO CONTROLS
# =========================================================

if st.session_state.last_response:

    st.divider()

    st.subheader(
        "🔊 الرد الصوتي"
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "▶  تشغيل آخر رد",
            use_container_width=True,
        ):

            if st.session_state.speaker:

                try:

                    st.session_state.speaker.speak(
                        st.session_state.last_response
                    )

                except Exception as e:

                    st.error(
                        str(e)
                    )


    with col2:

        if st.button(
            "■  إيقاف",
            use_container_width=True,
        ):

            if st.session_state.speaker:

                try:

                    st.session_state.speaker.stop()

                except Exception:

                    pass


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        CodeBox AI · Personal Assistant · Powered by Gemini
    </div>
    """,
    unsafe_allow_html=True,
)
