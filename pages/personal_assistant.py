
import io

import streamlit as st
import speech_recognition as sr

from utils.gemini_ai import GeminiAI
from utils.speaker import Speaker


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="CodeBox Personal Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# CSS
# ==================================================


st.markdown(
    """
    <style>

    /* =================================
       CODEBOX DARK BACKGROUND
    ================================= */

    .stApp {

        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(37, 99, 235, 0.16),
                transparent 32%
            ),

            radial-gradient(
                circle at 85% 15%,
                rgba(124, 58, 237, 0.13),
                transparent 30%
            ),

            radial-gradient(
                circle at 50% 100%,
                rgba(14, 116, 144, 0.10),
                transparent 35%
            ),

            #080b14;
    }


    /* =================================
       MAIN AREA
    ================================= */

    .block-container {

        max-width: 1200px;

        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =================================
       HEADER
    ================================= */

    .assistant-title {

        font-size: 44px;
        font-weight: 800;

        text-align: center;

        margin-top: 10px;
        margin-bottom: 5px;

        color: #e5edff;
    }


    .assistant-subtitle {

        text-align: center;

        font-size: 18px;

        color: #94a3b8;

        margin-bottom: 25px;
    }


    /* =================================
       CHAT
    ================================= */

    [data-testid="stChatMessage"] {

        background: rgba(15, 23, 42, 0.55);

        border: 1px solid rgba(
            96,
            165,
            250,
            0.10
        );

        border-radius: 16px;

        margin-bottom: 10px;
    }


    /* =================================
       CHAT INPUT
    ================================= */

    [data-testid="stChatInput"] {

        background: #0f172a;

        border: 1px solid rgba(
            96,
            165,
            250,
            0.25
        );

        border-radius: 16px;
    }


    /* =================================
       BUTTONS
    ================================= */

    .stButton > button {

        background: #111827;

        color: #e5edff;

        border: 1px solid rgba(
            96,
            165,
            250,
            0.22
        );

        border-radius: 12px;

        transition: all 0.2s ease;
    }


    .stButton > button:hover {

        background: #172554;

        border-color: #3b82f6;

        transform: translateY(-2px);
    }


    /* =================================
       SIDEBAR
    ================================= */

    [data-testid="stSidebar"] {

        background: #070a12;

        border-right: 1px solid rgba(
            96,
            165,
            250,
            0.15
        );
    }


    /* =================================
       DIVIDERS
    ================================= */

    hr {

        border-color: rgba(
            148,
            163,
            184,
            0.12
        );
    }


    /* =================================
       HEADINGS
    ================================= */

    h1, h2, h3 {

        color: #e5edff;
    }


    /* =================================
       CAPTIONS
    ================================= */

    .stCaption {

        color: #94a3b8;
    }


    </style>
    """,
    unsafe_allow_html=True,
)


    /* ==============================
       TITLE
    ============================== */

    .assistant-title {
        font-size: 44px;
        font-weight: 800;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;

        color: #60a5fa;
    }


    /* ==============================
       SUBTITLE
    ============================== */

    .assistant-subtitle {
        text-align: center;
        font-size: 18px;
        opacity: 0.75;
        margin-bottom: 25px;

        color: #93c5fd;
    }


    /* ==============================
       STATUS
    ============================== */

    .status-box {
        padding: 12px;
        border-radius: 12px;

        border: 1px solid rgba(96, 165, 250, 0.25);

        background: rgba(59, 130, 246, 0.05);

        text-align: center;
        margin-bottom: 15px;
    }


    /* ==============================
       BUTTONS
    ============================== */

    .stButton > button {

        border-radius: 12px;

        border: 1px solid rgba(
            96,
            165,
            250,
            0.25
        );

        background: rgba(
            59,
            130,
            246,
            0.06
        );

        transition: 0.2s ease;
    }


    .stButton > button:hover {

        border-color: #60a5fa;

        background: rgba(
            59,
            130,
            246,
            0.14
        );

        transform: translateY(-1px);
    }


    /* ==============================
       CHAT
    ============================== */

    [data-testid="stChatMessage"] {

        border-radius: 14px;

        border: 1px solid rgba(
            96,
            165,
            250,
            0.10
        );

        margin-bottom: 8px;
    }


    /* ==============================
       CHAT INPUT
    ============================== */

    [data-testid="stChatInput"] {

        border-radius: 14px;

        border: 1px solid rgba(
            96,
            165,
            250,
            0.20
        );
    }


    /* ==============================
       SIDEBAR
    ============================== */

    [data-testid="stSidebar"] {

        border-right: 1px solid rgba(
            96,
            165,
            250,
            0.15
        );
    }


    /* ==============================
       DIVIDER
    ============================== */

    hr {
        border-color: rgba(
            96,
            165,
            250,
            0.15
        );
    }


    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="assistant-title">'
    '🤖 CodeBox Personal Assistant'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="assistant-subtitle">'
    'تحدث، اكتب، واستمع — مساعدك الشخصي في CodeBox 🚀'
    '</div>',
    unsafe_allow_html=True,
)

st.divider()


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "last_response" not in st.session_state:

    st.session_state.last_response = None


# ==================================================
# GEMINI
# ==================================================

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


# ==================================================
# SPEAKER
# ==================================================

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


# ==================================================
# CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==================================================
# VOICE SECTION
# ==================================================

st.write("### 🎤 التحدث مع المساعد")


audio_value = st.audio_input(
    "🎤 اضغط وسجل رسالتك"
)


# ==================================================
# VOICE TO TEXT
# ==================================================

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

        with sr.AudioFile(
            audio_file
        ) as source:

            audio_data = (
                recognizer.record(source)
            )

        voice_text = (
            recognizer.recognize_google(
                audio_data,
                language="ar-EG",
            )
        )

        st.success(
            f"🎤 أنت قلت: {voice_text}"
        )

    except sr.UnknownValueError:

        st.warning(
            "❓ لم أستطع فهم كلامك."
        )

    except sr.RequestError as error:

        st.error(
            f"❌ مشكلة في خدمة التعرف على الصوت:\n{error}"
        )

    except Exception as error:

        st.error(
            f"❌ حدث خطأ أثناء معالجة الصوت:\n{error}"
        )


# ==================================================
# CHAT INPUT
# ==================================================

prompt = st.chat_input(
    "اكتب رسالتك هنا... 💬"
)


# ==================================================
# SELECT INPUT
# ==================================================

user_message = None


if voice_text:

    user_message = voice_text

elif prompt:

    user_message = prompt


# ==================================================
# SEND MESSAGE
# ==================================================

if user_message:

    if st.session_state.speaker:

        st.session_state.speaker.stop()


    # ----------------------------------------------
    # USER MESSAGE
    # ----------------------------------------------

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


    # ----------------------------------------------
    # GEMINI RESPONSE
    # ----------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "🤔 بفكر..."
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


        st.session_state.last_response = (
            response
        )


        # ------------------------------------------
        # AUTO SPEAK
        # ------------------------------------------

        if st.session_state.speaker:

            st.session_state.speaker.speak(
                response
            )


    # ----------------------------------------------
    # SAVE RESPONSE
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )


# ==================================================
# AUDIO CONTROL PANEL
# ==================================================

st.divider()

st.write("### 🔊 التحكم في الصوت")


audio_col1, audio_col2, audio_col3 = st.columns(
    3
)


# ==================================================
# PLAY
# ==================================================

with audio_col1:

    if st.button(
        "🔊 تشغيل الصوت",
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


# ==================================================
# STOP
# ==================================================

with audio_col2:

    if st.button(
        "🔇 إيقاف فورًا",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            st.session_state.speaker.stop()

            st.toast(
                "🔇 تم إيقاف الصوت فورًا"
            )


# ==================================================
# CLEAR CHAT
# ==================================================

with audio_col3:

    if st.button(
        "🗑️ مسح المحادثة",
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
            "🗑️ تم مسح المحادثة بالكامل"
        )

        st.rerun()


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title(
        "🤖 CodeBox Assistant"
    )

    st.write(
        "مساعدك الشخصي للبرمجة والتعلم."
    )

    st.divider()


    # ==================================================
    # STATUS
    # ==================================================

    st.write(
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


    # ==================================================
    # QUICK CONTROLS
    # ==================================================

    st.write(
        "### 🎛️ التحكم السريع"
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


    if st.button(
        "🔇 إيقاف الصوت",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            st.session_state.speaker.stop()


    st.divider()


    # ==================================================
    # INFO
    # ==================================================

    st.caption(
        "🎤 تحدث مع المساعد"
    )

    st.caption(
        "🔊 العربي والإنجليزي مدعومان"
    )

    st.caption(
        "🧠 مدعوم بواسطة Gemini"
    )

    st.caption(
        "🚀 CodeBox"
    )
