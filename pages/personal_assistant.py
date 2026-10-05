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
# STREAMLIT STYLE
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f4f7fb;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        margin-bottom: 10px;
        border: 1px solid #e2e8f0;
        background-color: #ffffff;
    }

    [data-testid="stChatInput"] > div {
        border-radius: 16px;
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
    }

    .stButton > button {
        border-radius: 12px;
        min-height: 42px;
        border: 1px solid #dbe3ee;
        background-color: #ffffff;
        color: #1e293b;
        font-weight: 600;
    }

    .stButton > button:hover {
        border-color: #2563eb;
        color: #2563eb;
        background-color: #f8fbff;
    }

    hr {
        border-color: #e2e8f0;
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

    st.title("🤖 CodeBox AI")

    st.caption(
        "Personal AI Assistant"
    )

    st.divider()

    st.subheader("⚙️ التحكم")

    if st.button(
        "🆕 محادثة جديدة",
        use_container_width=True
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
        "🔇 إيقاف الصوت",
        use_container_width=True
    ):

        if st.session_state.speaker:

            try:
                st.session_state.speaker.stop()
            except Exception:
                pass


    st.divider()

    st.subheader("✨ المميزات")

    st.write("💬 محادثة ذكية")
    st.write("🐍 Python")
    st.write("💻 Programming")
    st.write("🤖 Artificial Intelligence")
    st.write("🐞 Debugging")
    st.write("🎤 Voice Input")
    st.write("🔊 Voice Response")

    st.divider()

    st.caption(
        "CodeBox AI"
    )


# =========================================================
# HEADER
# =========================================================

st.title("🤖 CodeBox AI")

st.caption(
    "مساعدك الشخصي الذكي للبرمجة والتكنولوجيا"
)


# =========================================================
# STATUS
# =========================================================

if st.session_state.speaker:

    try:

        if st.session_state.speaker.is_playing():

            st.success(
                "🔊 المساعد يتحدث الآن"
            )

        else:

            st.info(
                "🟢 المساعد جاهز"
            )

    except Exception:

        st.info(
            "🟢 المساعد جاهز"
        )

else:

    st.info(
        "🟢 المساعد جاهز"
    )


# =========================================================
# START SCREEN
# =========================================================

if not st.session_state.messages:

    st.subheader(
        "👋 أهلاً بك"
    )

    st.write(
        "اكتب أي سؤال وسيقوم CodeBox AI بمساعدتك."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "🐍 Python\n\n"
            "كتابة وشرح الأكواد"
        )

    with col2:

        st.info(
            "🤖 AI\n\n"
            "الذكاء الاصطناعي"
        )

    with col3:

        st.info(
            "🐞 Debugging\n\n"
            "حل مشاكل الكود"
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
# TEXT INPUT
# =========================================================

prompt = st.chat_input(
    "اكتب رسالتك هنا..."
)


# =========================================================
# VOICE INPUT
# =========================================================

st.divider()

st.subheader(
    "🎤 التحدث مع المساعد"
)

audio_value = st.audio_input(
    "اضغط للتسجيل"
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
            "🎧 جاري تحويل الصوت إلى نص..."
        ):

            voice_text = recognizer.recognize_google(
                audio_data,
                language="ar-EG"
            )

        st.success(
            f"النص: {voice_text}"
        )

    except sr.UnknownValueError:

        st.error(
            "لم أتمكن من فهم التسجيل."
        )

    except sr.RequestError:

        st.error(
            "حدثت مشكلة في خدمة تحويل الصوت."
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
            "content": user_message
        }
    )

    with st.chat_message("user"):

        st.markdown(
            user_message
        )


    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 CodeBox AI يفكر..."
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
                        "content": response
                    }
                )

                st.session_state.last_response = response


                # =============================================
                # SPEAK RESPONSE
                # =============================================

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
                        "content": error_message
                    }
                )


# =========================================================
# AUDIO CONTROLS
# =========================================================

if st.session_state.last_response:

    st.divider()

    st.subheader(
        "🔊 التحكم في الرد"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "▶️ تشغيل آخر رد",
            use_container_width=True
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
            "⏹️ إيقاف الصوت",
            use_container_width=True
        ):

            if st.session_state.speaker:

                try:

                    st.session_state.speaker.stop()

                except Exception:
                    pass


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "CodeBox AI • Personal Assistant • Gemini"
)
