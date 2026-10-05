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
# PROFESSIONAL AI STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* ================================
       GLOBAL
       ================================ */

    .stApp {
        background:
            radial-gradient(
                circle at 50% -20%,
                rgba(99, 102, 241, 0.16),
                transparent 35%
            ),
            #080b12;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 6rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ================================
       SIDEBAR
       ================================ */

    section[data-testid="stSidebar"] {
        background: #090c13;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }


    /* ================================
       TOP BRAND
       ================================ */

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 5px;
    }

    .brand-icon {
        width: 46px;
        height: 46px;
        border-radius: 14px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 23px;

        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            );

        box-shadow:
            0 0 25px rgba(99,102,241,0.25);
    }

    .brand-name {
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .brand-name span {
        color: #818cf8;
    }

    .brand-subtitle {
        color: #71798a;
        font-size: 13px;
        margin-left: 58px;
        margin-top: -8px;
    }


    /* ================================
       HERO
       ================================ */

    .hero {
        text-align: center;
        padding: 40px 20px 25px;
    }

    .hero-orb {
        width: 78px;
        height: 78px;
        margin: 0 auto 20px;

        border-radius: 24px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 38px;

        background:
            linear-gradient(
                145deg,
                #6366f1,
                #7c3aed
            );

        box-shadow:
            0 0 40px rgba(99,102,241,0.28),
            inset 0 1px 0 rgba(255,255,255,0.2);
    }

    .hero-title {
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }

    .hero-description {
        color: #8b93a4;
        font-size: 15px;
        max-width: 580px;
        margin: auto;
        line-height: 1.7;
    }


    /* ================================
       STATUS
       ================================ */

    .status {
        width: fit-content;
        margin: 10px auto 25px;

        padding: 7px 14px;

        border-radius: 30px;

        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(34,197,94,0.18);

        color: #86efac;
        font-size: 12px;
        font-weight: 600;
    }


    /* ================================
       FEATURE CHIPS
       ================================ */

    .chips {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 8px;
        margin: 15px auto 30px;
    }

    .chip {
        padding: 7px 12px;

        border-radius: 10px;

        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.07);

        color: #aab2c2;
        font-size: 12px;
    }


    /* ================================
       CHAT
       ================================ */

    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.055);

        border-radius: 18px;

        padding: 12px 16px;

        margin-bottom: 12px;
    }

    [data-testid="stChatMessage"]:hover {
        border-color: rgba(129,140,248,0.15);
    }


    /* ================================
       CHAT INPUT
       ================================ */

    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 22px;
        left: 50%;
        transform: translateX(-50%);

        width: min(850px, 75vw);

        z-index: 999;
    }

    [data-testid="stChatInput"] > div {
        background: #111620 !important;

        border: 1px solid #252c3a !important;

        border-radius: 18px !important;

        box-shadow:
            0 12px 45px rgba(0,0,0,0.35),
            0 0 0 1px rgba(99,102,241,0.03);
    }

    [data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
    }


    /* ================================
       BUTTONS
       ================================ */

    .stButton > button {
        border-radius: 12px !important;

        min-height: 42px;

        background: #111620 !important;

        color: #dce2ef !important;

        border: 1px solid #252c3a !important;

        font-weight: 600;

        transition:
            background 0.2s ease,
            border 0.2s ease,
            transform 0.2s ease;
    }

    .stButton > button:hover {
        background: #171d2a !important;

        border-color: #6366f1 !important;

        transform: translateY(-1px);
    }


    /* ================================
       AUDIO
       ================================ */

    [data-testid="stAudioInput"] {
        border-radius: 14px;
    }


    /* ================================
       DIVIDERS
       ================================ */

    hr {
        border: none !important;
        border-top: 1px solid rgba(255,255,255,0.06) !important;
        margin: 25px 0 !important;
    }


    /* ================================
       SIDEBAR ITEMS
       ================================ */

    .side-title {
        font-size: 12px;
        color: #687184;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 20px 0 10px;
    }

    .side-feature {
        padding: 10px 12px;
        margin-bottom: 6px;

        border-radius: 10px;

        background: rgba(255,255,255,0.025);

        color: #aab2c2;

        font-size: 13px;
    }


    /* ================================
       FOOTER
       ================================ */

    .mini-footer {
        text-align: center;

        color: #4f5869;

        font-size: 11px;

        margin-top: 30px;
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

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "assistant" not in st.session_state:
    st.session_state.assistant = None

if "speaker" not in st.session_state:
    st.session_state.speaker = None


# =========================================================
# INITIALIZE GEMINI
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
        <div class="brand">
            <div class="brand-icon">🤖</div>
            <div class="brand-name">
                Code<span>Box</span>
            </div>
        </div>

        <div class="brand-subtitle">
            Personal AI Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div class="side-title">Workspace</div>',
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
        '<div class="side-title">Capabilities</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="side-feature">✦ Gemini AI</div>
        <div class="side-feature">✦ Programming Assistant</div>
        <div class="side-feature">✦ Voice Input</div>
        <div class="side-feature">✦ Voice Response</div>
        <div class="side-feature">✦ Debugging</div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption(
        "CodeBox AI • Intelligent Workspace"
    )


# =========================================================
# MAIN HERO
# =========================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="hero">

            <div class="hero-orb">
                🤖
            </div>

            <div class="hero-title">
                CodeBox AI
            </div>

            <div class="hero-description">
                مساعدك الشخصي الذكي للبرمجة والتكنولوجيا،
                مدعوم بتقنيات Gemini AI.
            </div>

            <div class="status">
                ● AI ONLINE
            </div>

        </div>

        <div class="chips">

            <div class="chip">🐍 Python</div>
            <div class="chip">💻 Programming</div>
            <div class="chip">🤖 AI</div>
            <div class="chip">🐞 Debugging</div>
            <div class="chip">🎤 Voice</div>

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
    "🎙️ التحدث مع المساعد",
    expanded=False,
):

    st.caption(
        "سجل رسالتك الصوتية وسيتم تحويلها إلى نص."
    )

    audio_value = st.audio_input(
        "تسجيل رسالة"
    )

    voice_text = None

    if audio_value is not None:

        try:

            recognizer = sr.Recognizer()

            audio_bytes = audio_value.getvalue()

            audio_file = io.BytesIO(
                audio_bytes
            )

            with sr.AudioFile(audio_file) as source:

                audio_data = recognizer.record(
                    source
                )

            with st.spinner(
                "جاري تحويل الصوت إلى نص..."
            ):

                voice_text = recognizer.recognize_google(
                    audio_data,
                    language="ar-EG",
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
                "خدمة تحويل الصوت غير متاحة حاليًا."
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

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    # Show user message
    with st.chat_message("user"):

        st.markdown(
            user_message
        )


    # Generate AI response
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

                # Save response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )

                st.session_state.last_response = response


                # Voice response
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
# RESPONSE CONTROLS
# =========================================================

if st.session_state.last_response:

    st.divider()

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
            "■  إيقاف الرد",
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
    <div class="mini-footer">
        CodeBox AI · Personal Assistant · Powered by Gemini
    </div>
    """,
    unsafe_allow_html=True,
)
