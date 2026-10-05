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
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ================================
       GLOBAL
    ================================= */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(80, 80, 255, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(0, 220, 255, 0.06),
                transparent 30%
            );
    }

    /* Hide Streamlit default elements */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }


    /* ================================
       MAIN HEADER
    ================================= */

    .codebox-header {
        padding: 25px 20px 15px 20px;
        text-align: center;
    }

    .codebox-logo {
        font-size: 48px;
        margin-bottom: 5px;
    }

    .codebox-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
    }

    .codebox-title span {
        background: linear-gradient(
            90deg,
            #7c5cff,
            #00d4ff
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .codebox-subtitle {
        margin-top: 8px;
        font-size: 16px;
        opacity: 0.65;
    }


    /* ================================
       AI STATUS
    ================================= */

    .ai-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;

        padding: 7px 15px;

        margin-top: 12px;

        border-radius: 30px;

        background: rgba(0, 200, 120, 0.08);

        border: 1px solid rgba(0, 200, 120, 0.25);

        font-size: 13px;
    }

    .status-dot {
        width: 8px;
        height: 8px;

        background: #00d084;

        border-radius: 50%;

        display: inline-block;
    }


    /* ================================
       CHAT AREA
    ================================= */

    [data-testid="stChatMessage"] {
        border-radius: 18px;

        padding: 8px 12px;

        margin-top: 10px;
        margin-bottom: 10px;
    }

    [data-testid="stChatMessage"] p {
        font-size: 15px;
        line-height: 1.8;
    }


    /* ================================
       CHAT INPUT
    ================================= */

    [data-testid="stChatInput"] {
        padding-top: 10px;
    }

    [data-testid="stChatInput"] textarea {
        border-radius: 18px !important;
        padding: 15px !important;
    }


    /* ================================
       SECTION CARD
    ================================= */

    .section-card {
        padding: 20px;

        border-radius: 20px;

        border: 1px solid rgba(128,128,128,0.18);

        background: rgba(128,128,128,0.04);

        margin-top: 15px;
        margin-bottom: 15px;
    }


    .section-title {
        font-size: 20px;
        font-weight: 700;

        margin-bottom: 12px;
    }


    .section-description {
        opacity: 0.65;
        font-size: 14px;
    }


    /* ================================
       SIDEBAR
    ================================= */

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.15);
    }

    .sidebar-brand {
        text-align: center;

        padding: 10px 5px 20px 5px;
    }

    .sidebar-brand-icon {
        font-size: 42px;
    }

    .sidebar-brand-title {
        font-size: 22px;
        font-weight: 800;
    }

    .sidebar-brand-subtitle {
        font-size: 12px;
        opacity: 0.55;
    }


    /* ================================
       BUTTONS
    ================================= */

    .stButton > button {
        border-radius: 12px;

        min-height: 42px;

        font-weight: 600;

        transition:
            transform 0.15s ease,
            border-color 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }


    /* ================================
       VOICE BOX
    ================================= */

    .voice-header {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .voice-description {
        font-size: 13px;
        opacity: 0.6;
        margin-bottom: 15px;
    }


    /* ================================
       FOOTER
    ================================= */

    .codebox-footer {
        text-align: center;

        margin-top: 35px;

        padding: 15px;

        font-size: 12px;

        opacity: 0.45;
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


# =========================================================
# GEMINI INITIALIZATION
# =========================================================

if "assistant" not in st.session_state:

    try:

        st.session_state.assistant = GeminiAI()

    except Exception as error:

        st.error(
            f"""
            ❌ حدث خطأ أثناء تشغيل Gemini:

            {error}
            """
        )

        st.stop()


# =========================================================
# SPEAKER INITIALIZATION
# =========================================================

if "speaker" not in st.session_state:

    try:

        st.session_state.speaker = Speaker()

    except Exception as error:

        st.error(
            f"""
            ❌ حدث خطأ في نظام الصوت:

            {error}
            """
        )

        st.session_state.speaker = None


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="codebox-header">

        <div class="codebox-logo">
            🤖
        </div>

        <div class="codebox-title">
            <span>CodeBox AI</span>
        </div>

        <div class="codebox-subtitle">
            مساعدك الذكي للبرمجة والتكنولوجيا والتعلم
        </div>

        <div class="ai-status">
            <span class="status-dot"></span>
            Gemini AI متصل وجاهز
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


st.divider()


# =========================================================
# WELCOME MESSAGE
# =========================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="section-card">

            <div class="section-title">
                👋 أهلاً بك في CodeBox AI
            </div>

            <div class="section-description">
                اسألني عن البرمجة، Python، JavaScript،
                HTML، CSS، قواعد البيانات، الأخطاء البرمجية
                أو أي موضوع تكنولوجي.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    role = message["role"]

    avatar = "👤" if role == "user" else "🤖"

    with st.chat_message(
        role,
        avatar=avatar,
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# VOICE SECTION
# =========================================================

st.markdown(
    """
    <div class="section-card">

        <div class="voice-header">
            🎤 التحدث مع CodeBox AI
        </div>

        <div class="voice-description">
            سجل رسالتك صوتيًا وسيقوم المساعد بتحويلها إلى نص والرد عليك.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


audio_value = st.audio_input(
    "🎙️ اضغط هنا لتسجيل رسالة",
)


# =========================================================
# VOICE TO TEXT
# =========================================================

voice_text = None


if audio_value is not None:

    try:

        recognizer = sr.Recognizer()

        audio_bytes = audio_value.getvalue()

        audio_file = io.BytesIO(
            audio_bytes
        )

        with sr.AudioFile(
            audio_file
        ) as source:

            audio_data = recognizer.record(
                source
            )

        voice_text = recognizer.recognize_google(
            audio_data,
            language="ar-EG",
        )

        st.success(
            f"🎤 تم التعرف على كلامك: {voice_text}"
        )

    except sr.UnknownValueError:

        st.warning(
            "❓ لم أستطع فهم التسجيل الصوتي."
        )

    except sr.RequestError as error:

        st.error(
            f"❌ مشكلة في خدمة التعرف على الصوت: {error}"
        )

    except Exception as error:

        st.error(
            f"❌ حدث خطأ أثناء معالجة الصوت: {error}"
        )


# =========================================================
# CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "💬 اكتب رسالتك إلى CodeBox AI..."
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

    # Stop previous audio

    if st.session_state.speaker:

        st.session_state.speaker.stop()


    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )


    # =====================================================
    # DISPLAY USER MESSAGE
    # =====================================================

    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(
            user_message
        )


    # =====================================================
    # GENERATE AI RESPONSE
    # =====================================================

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        with st.spinner(
            "🤖 CodeBox AI يفكر..."
        ):

            response = (
                st.session_state
                .assistant
                .generate_response(
                    user_message
                )
            )


        st.markdown(
            response
        )


        # Save last response

        st.session_state.last_response = response


        # =================================================
        # SPEAK RESPONSE
        # =================================================

        if st.session_state.speaker:

            st.session_state.speaker.speak(
                response
            )


    # =====================================================
    # SAVE AI MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )


# =========================================================
# AUDIO CONTROL
# =========================================================

st.divider()

st.markdown(
    """
    <div class="section-card">

        <div class="section-title">
            🔊 التحكم في الصوت
        </div>

        <div class="section-description">
            تحكم في صوت آخر رد من CodeBox AI.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


audio_col1, audio_col2, audio_col3 = st.columns(
    3
)


# =========================================================
# PLAY
# =========================================================

with audio_col1:

    if st.button(
        "🔊 تشغيل آخر رد",
        use_container_width=True,
    ):

        if (
            st.session_state.speaker
            and st.session_state.last_response
        ):

            st.session_state.speaker.speak(
                st.session_state.last_response
            )

            st.toast(
                "🔊 يتم تشغيل آخر رد"
            )

        else:

            st.info(
                "لا يوجد رد لتشغيله."
            )


# =========================================================
# STOP
# =========================================================

with audio_col2:

    if st.button(
        "🔇 إيقاف الصوت",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            st.session_state.speaker.stop()

            st.toast(
                "🔇 تم إيقاف الصوت"
            )


# =========================================================
# CLEAR CHAT
# =========================================================

with audio_col3:

    if st.button(
        "🗑️ محادثة جديدة",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            st.session_state.speaker.stop()


        st.session_state.messages = []

        st.session_state.last_response = None


        try:

            st.session_state.assistant.reset_chat()

        except Exception:

            pass


        st.toast(
            "✨ بدأت محادثة جديدة"
        )

        st.rerun()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">

            <div class="sidebar-brand-icon">
                🤖
            </div>

            <div class="sidebar-brand-title">
                CodeBox AI
            </div>

            <div class="sidebar-brand-subtitle">
                Personal Assistant
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.divider()


    # =====================================================
    # STATUS
    # =====================================================

    st.markdown(
        "### 📊 حالة المساعد"
    )


    if st.session_state.speaker:

        if st.session_state.speaker.is_playing():

            st.warning(
                "🗣️ المساعد يتحدث الآن"
            )

        else:

            st.success(
                "🟢 المساعد جاهز"
            )

    else:

        st.error(
            "🔴 نظام الصوت غير متاح"
        )


    st.divider()


    # =====================================================
    # QUICK CONTROLS
    # =====================================================

    st.markdown(
        "### 🎛️ تحكم سريع"
    )


    if st.button(
        "🔊 تشغيل آخر رد",
        use_container_width=True,
    ):

        if (
            st.session_state.speaker
            and st.session_state.last_response
        ):

            st.session_state.speaker.speak(
                st.session_state.last_response
            )

            st.toast(
                "🔊 تشغيل آخر رد"
            )


    if st.button(
        "🔇 إيقاف الصوت",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            st.session_state.speaker.stop()

            st.toast(
                "🔇 تم إيقاف الصوت"
            )


    if st.button(
        "🗑️ محادثة جديدة",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            st.session_state.speaker.stop()


        st.session_state.messages = []

        st.session_state.last_response = None


        try:

            st.session_state.assistant.reset_chat()

        except Exception:

            pass


        st.toast(
            "✨ تم إنشاء محادثة جديدة"
        )

        st.rerun()


    st.divider()


    # =====================================================
    # FEATURES
    # =====================================================

    st.markdown(
        "### ✨ المميزات"
    )

    st.caption(
        "🐍 Python"
    )

    st.caption(
        "🌐 HTML / CSS / JavaScript"
    )

    st.caption(
        "💻 C++ / Java"
    )

    st.caption(
        "🗄️ SQL وقواعد البيانات"
    )

    st.caption(
        "🐞 Debugging وحل الأخطاء"
    )

    st.caption(
        "🎤 دعم الصوت"
    )

    st.caption(
        "🧠 Gemini AI"
    )


    st.divider()


    st.caption(
        "🚀 CodeBox"
    )

    st.caption(
        "Built for learning & coding"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="codebox-footer">
        🤖 CodeBox AI • Powered by Gemini • Built with Python & Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
