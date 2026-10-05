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

    .assistant-title {
        font-size: 44px;
        font-weight: 800;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .assistant-subtitle {
        text-align: center;
        font-size: 18px;
        opacity: 0.75;
        margin-bottom: 25px;
    }

    .status-box {
        padding: 12px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        text-align: center;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    """
    <div class="assistant-title">
        🤖 CodeBox Personal Assistant
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="assistant-subtitle">
        تحدث، اكتب، واستمع — مساعدك الشخصي في CodeBox 🚀
    </div>
    """,
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

    # Stop old audio
    if st.session_state.speaker:

        st.session_state.speaker.stop()


    # ----------------------------------------------
    # User message
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
    # Gemini response
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


        # Save last response
        st.session_state.last_response = (
            response
        )


        # Speak automatically
        if st.session_state.speaker:

            st.session_state.speaker.speak(
                response
            )


    # ----------------------------------------------
    # Save assistant message
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

        # Stop audio
        if st.session_state.speaker:

            st.session_state.speaker.stop()


        # Clear messages
        st.session_state.messages = []


        # Clear last response
        st.session_state.last_response = None


        # Reset Gemini
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
    