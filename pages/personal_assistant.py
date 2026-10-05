import io
import streamlit as st
import speech_recognition as sr

from utils.gemini_ai import GeminiAI
from utils.speaker import Speaker


# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="CodeBox AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================
# Custom Style
# =========================
st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #0b0f19;
    }

    /* Main container */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .main-subtitle {
        color: #9ca3af;
        font-size: 17px;
        margin-bottom: 25px;
    }

    /* Cards */
    .info-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        border-radius: 18px;
        margin-bottom: 12px;
        padding: 8px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        min-height: 42px;
        font-weight: 600;
        border: 1px solid #374151;
        background: #151b29;
        transition: 0.2s;
    }

    .stButton > button:hover {
        border-color: #6366f1;
        background: #1d2435;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        border-radius: 16px;
    }

    /* Audio input */
    [data-testid="stAudioInput"] {
        border-radius: 14px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #080c14;
        border-right: 1px solid #1f2937;
    }

    /* Divider */
    hr {
        border-color: #1f2937;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# Session State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "assistant" not in st.session_state:
    st.session_state.assistant = None

if "speaker" not in st.session_state:
    st.session_state.speaker = None


# =========================
# Initialize AI
# =========================
if st.session_state.assistant is None:
    try:
        st.session_state.assistant = GeminiAI()
    except Exception as e:
        st.error(f"حدث خطأ أثناء تشغيل Gemini AI:\n{e}")
        st.stop()


# =========================
# Initialize Speaker
# =========================
if st.session_state.speaker is None:
    try:
        st.session_state.speaker = Speaker()
    except Exception as e:
        st.warning(f"تعذر تشغيل الصوت: {e}")


# =========================
# Header
# =========================
st.markdown(
    '<div class="main-title">🤖 CodeBox AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'مساعدك الشخصي للبرمجة والتكنولوجيا وحل المشاكل'
    '</div>',
    unsafe_allow_html=True
)


# =========================
# Status
# =========================
if st.session_state.speaker:
    try:
        playing = st.session_state.speaker.is_playing()
    except Exception:
        playing = False
else:
    playing = False


if playing:
    st.success("🔊 المساعد يتحدث الآن")
else:
    st.info("🟢 المساعد جاهز")


# =========================
# Conversation
# =========================
if st.session_state.messages:

    st.subheader("💬 المحادثة")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

else:

    st.markdown(
        """
        <div class="info-card">

        ## 👋 أهلاً بك في CodeBox AI

        أنا مساعدك الشخصي الذكي.

        يمكنك سؤالي عن:
        
        - 🐍 Python
        - 💻 C++ / Java
        - 🌐 JavaScript
        - 🗄️ SQL
        - 🤖 Artificial Intelligence
        - 🐞 Debugging
        - 🧠 البرمجة والتكنولوجيا

        اكتب سؤالك في الأسفل وابدأ المحادثة.

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# Text Input
# =========================
prompt = st.chat_input(
    "اكتب رسالتك هنا..."
)


# =========================
# Voice Section
# =========================
st.divider()

st.subheader("🎙️ التحدث مع المساعد")

st.caption(
    "بدل ما تكتب، سجل رسالتك وسيتم تحويلها إلى نص."
)

audio_value = st.audio_input(
    "🎤 تسجيل رسالة صوتية"
)

voice_text = None


if audio_value is not None:

    try:

        recognizer = sr.Recognizer()

        audio_bytes = audio_value.getvalue()

        audio_file = io.BytesIO(audio_bytes)

        with sr.AudioFile(audio_file) as source:

            audio_data = recognizer.record(source)

        with st.spinner("🎧 جاري تحويل الصوت إلى نص..."):

            voice_text = recognizer.recognize_google(
                audio_data,
                language="ar-EG"
            )

        st.success(f"تم التعرف على الكلام: {voice_text}")

    except sr.UnknownValueError:

        st.error(
            "لم أتمكن من فهم الصوت، حاول التسجيل مرة أخرى."
        )

    except sr.RequestError:

        st.error(
            "حدثت مشكلة في خدمة تحويل الصوت إلى نص."
        )

    except Exception as e:

        st.error(
            f"حدث خطأ أثناء معالجة الصوت:\n{e}"
        )


# =========================
# Select User Message
# =========================
user_message = voice_text if voice_text else prompt


# =========================
# Send Message
# =========================
if user_message:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("🤖 يفكر..."):

            try:

                response = (
                    st.session_state.assistant
                    .generate_response(user_message)
                )

                st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

                st.session_state.last_response = response

                # Speak response
                if st.session_state.speaker:

                    try:

                        st.session_state.speaker.speak(
                            response
                        )

                    except Exception as e:

                        st.warning(
                            f"تعذر تشغيل الرد الصوتي: {e}"
                        )

            except Exception as e:

                error_message = (
                    f"حدث خطأ أثناء الحصول على الرد:\n\n{e}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )


# =========================
# Audio Controls
# =========================
if st.session_state.last_response:

    st.divider()

    st.subheader("🔊 التحكم في الصوت")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "▶️ تشغيل الرد",
            use_container_width=True
        ):

            if st.session_state.speaker:

                try:

                    st.session_state.speaker.speak(
                        st.session_state.last_response
                    )

                except Exception as e:

                    st.error(
                        f"حدث خطأ: {e}"
                    )

    with col2:

        if st.button(
            "⏹️ إيقاف الصوت",
            use_container_width=True
        ):

            if st.session_state.speaker:

                try:

                    st.session_state.speaker.stop()

                except Exception as e:

                    st.error(
                        f"حدث خطأ: {e}"
                    )

    with col3:

        if st.button(
            "🗑️ مسح المحادثة",
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


# =========================
# Sidebar
# =========================
with st.sidebar:

    st.markdown("## 🤖 CodeBox AI")

    st.caption(
        "Personal AI Assistant"
    )

    st.divider()

    st.markdown("### ⚡ الحالة")

    if playing:
        st.success("🔊 يتحدث")
    else:
        st.success("🟢 متصل")

    st.divider()

    st.markdown("### 🛠️ الأدوات")

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

    st.markdown("### ✨ المميزات")

    st.write("💬 محادثة ذكية")
    st.write("🎤 إدخال صوتي")
    st.write("🔊 رد صوتي")
    st.write("🧠 Gemini AI")
    st.write("💻 مساعد للبرمجة")
    st.write("🐞 Debugging")

    st.divider()

    st.caption(
        "CodeBox • Personal Assistant"
    )
