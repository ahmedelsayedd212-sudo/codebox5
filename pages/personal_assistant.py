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
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       GENERAL
    ========================= */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =========================
       HEADER
    ========================= */

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .main-subtitle {
        text-align: center;
        font-size: 16px;
        opacity: 0.65;
        margin-bottom: 20px;
    }


    /* =========================
       STATUS
    ========================= */

    .status {
        text-align: center;
        font-size: 14px;
        margin-bottom: 20px;
    }


    /* =========================
       SIDEBAR
    ========================= */

    .sidebar-title {
        text-align: center;
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sidebar-subtitle {
        text-align: center;
        font-size: 13px;
        opacity: 0.6;
        margin-bottom: 20px;
    }


    /* =========================
       CHAT
    ========================= */

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        margin-bottom: 10px;
    }

    [data-testid="stChatMessage"] p {
        line-height: 1.8;
    }


    /* =========================
       BUTTONS
    ========================= */

    .stButton > button {
        border-radius: 12px;
        min-height: 42px;
        font-weight: 600;
    }


    /* =========================
       FOOTER
    ========================= */

    .app-footer {
        text-align: center;
        margin-top: 30px;
        font-size: 12px;
        opacity: 0.5;
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

    except Exception as error:

        st.error("❌ حدث خطأ أثناء تشغيل Gemini.")
        st.code(str(error))

        st.stop()


# =========================================================
# INITIALIZE SPEAKER
# =========================================================

if st.session_state.speaker is None:

    try:
        st.session_state.speaker = Speaker()

    except Exception as error:

        st.warning("⚠️ نظام الصوت غير متاح.")
        st.session_state.speaker = None


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 CodeBox AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-subtitle">مساعدك الذكي للبرمجة والتكنولوجيا والتعلم</div>',
    unsafe_allow_html=True,
)

if st.session_state.speaker:

    if st.session_state.speaker.is_playing():

        st.markdown(
            '<div class="status">🟡 المساعد يتحدث الآن</div>',
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            '<div class="status">🟢 CodeBox AI جاهز</div>',
            unsafe_allow_html=True,
        )

else:

    st.markdown(
        '<div class="status">🟢 CodeBox AI جاهز — الصوت غير متاح</div>',
        unsafe_allow_html=True,
    )


st.divider()


# =========================================================
# WELCOME
# =========================================================

if not st.session_state.messages:

    st.info(
        """
        👋 **أهلاً بك في CodeBox AI**

        يمكنك سؤالي عن:

        🐍 Python  
        💻 C++ و Java  
        🌐 HTML و CSS و JavaScript  
        🗄️ SQL وقواعد البيانات  
        🐞 حل الأخطاء البرمجية  
        🤖 الذكاء الاصطناعي  
        📚 الدراسة والتعلم
        """
    )


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        avatar = "👤"

    else:

        avatar = "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar,
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# VOICE INPUT
# =========================================================

st.subheader("🎤 التحدث مع CodeBox AI")

st.caption(
    "سجل رسالتك الصوتية وسيتم تحويلها إلى نص."
)


audio_value = st.audio_input(
    "اضغط هنا لتسجيل رسالة"
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
            f"🎤 أنت قلت: {voice_text}"
        )

    except sr.UnknownValueError:

        st.warning(
            "❓ لم أستطع فهم التسجيل."
        )

    except sr.RequestError as error:

        st.error(
            "❌ خدمة التعرف على الصوت غير متاحة."
        )

        st.code(str(error))

    except Exception as error:

        st.error(
            "❌ حدث خطأ أثناء معالجة الصوت."
        )

        st.code(str(error))


# =========================================================
# TEXT INPUT
# =========================================================

prompt = st.chat_input(
    "💬 اكتب رسالتك هنا..."
)


# =========================================================
# SELECT USER MESSAGE
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

    # ---------------------------------------------
    # Stop previous speech
    # ---------------------------------------------

    if st.session_state.speaker:

        try:
            st.session_state.speaker.stop()

        except Exception:
            pass


    # ---------------------------------------------
    # Save user message
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )


    # ---------------------------------------------
    # Show user message
    # ---------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(
            user_message
        )


    # ---------------------------------------------
    # Generate AI response
    # ---------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        with st.spinner(
            "🤖 CodeBox AI يفكر..."
        ):

            try:

                response = (
                    st.session_state
                    .assistant
                    .generate_response(
                        user_message
                    )
                )

            except Exception as error:

                response = (
                    "❌ حدث خطأ أثناء الحصول على رد من Gemini.\n\n"
                    + str(error)
                )


        st.markdown(
            response
        )


    # ---------------------------------------------
    # Save response
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    st.session_state.last_response = response


    # ---------------------------------------------
    # Speak response
    # ---------------------------------------------

    if st.session_state.speaker:

        try:

            st.session_state.speaker.speak(
                response
            )

        except Exception as error:

            st.warning(
                "⚠️ لم يتم تشغيل الصوت."
            )


# =========================================================
# AUDIO CONTROLS
# =========================================================

st.divider()

st.subheader("🔊 التحكم في الصوت")

st.caption(
    "تحكم في صوت آخر رد من CodeBox AI."
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

            try:

                st.session_state.speaker.speak(
                    st.session_state.last_response
                )

                st.toast(
                    "🔊 يتم تشغيل آخر رد"
                )

            except Exception as error:

                st.error(
                    "❌ حدث خطأ أثناء تشغيل الصوت."
                )

                st.code(str(error))

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

            try:

                st.session_state.speaker.stop()

                st.toast(
                    "🔇 تم إيقاف الصوت"
                )

            except Exception as error:

                st.error(
                    "❌ حدث خطأ أثناء إيقاف الصوت."
                )

                st.code(str(error))

        else:

            st.info(
                "نظام الصوت غير متاح."
            )


# =========================================================
# NEW CHAT
# =========================================================

with audio_col3:

    if st.button(
        "🗑️ محادثة جديدة",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            try:
                st.session_state.speaker.stop()

            except Exception:
                pass


        st.session_state.messages = []

        st.session_state.last_response = None


        # Reset Gemini chat

        try:

            st.session_state.assistant.reset_chat()

        except Exception:
            pass


        st.toast(
            "✨ تم إنشاء محادثة جديدة"
        )

        st.rerun()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🤖 CodeBox AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-subtitle">Personal Assistant</div>',
        unsafe_allow_html=True,
    )


    st.divider()


    # =====================================================
    # STATUS
    # =====================================================

    st.subheader("📊 حالة المساعد")


    if st.session_state.speaker:

        try:

            playing = (
                st.session_state
                .speaker
                .is_playing()
            )

        except Exception:

            playing = False


        if playing:

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

    st.subheader("🎛️ التحكم السريع")


    if st.button(
        "🔊 تشغيل آخر رد",
        use_container_width=True,
    ):

        if (
            st.session_state.speaker
            and st.session_state.last_response
        ):

            try:

                st.session_state.speaker.speak(
                    st.session_state.last_response
                )

                st.toast(
                    "🔊 تشغيل آخر رد"
                )

            except Exception as error:

                st.error(
                    "❌ حدث خطأ في الصوت."
                )

                st.code(str(error))

        else:

            st.info(
                "لا يوجد رد لتشغيله."
            )


    if st.button(
        "🔇 إيقاف الصوت",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            try:

                st.session_state.speaker.stop()

                st.toast(
                    "🔇 تم إيقاف الصوت"
                )

            except Exception:
                pass


    if st.button(
        "🗑️ محادثة جديدة",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            try:
                st.session_state.speaker.stop()

            except Exception:
                pass


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

    st.subheader("✨ المميزات")

    st.write("🐍 Python")
    st.write("💻 C++ / Java")
    st.write("🌐 HTML / CSS / JavaScript")
    st.write("🗄️ SQL")
    st.write("🐞 Debugging")
    st.write("🎤 Voice Input")
    st.write("🔊 Text To Speech")
    st.write("🧠 Gemini AI")


    st.divider()


    st.caption(
        "🚀 CodeBox"
    )

    st.caption(
        "Built with Python + Streamlit"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="app-footer">🤖 CodeBox AI • Powered by Gemini</div>',
    unsafe_allow_html=True,
)
