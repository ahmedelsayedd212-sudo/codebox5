
import io

import streamlit as st
import speech_recognition as sr

from utils.gemini_ai import GeminiAI
from utils.speaker import Speaker


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="CodeBox AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# STYLE
# ==================================================

st.markdown(
    """
    <style>

    /* ==============================
       APP
    ============================== */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(80, 110, 255, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(150, 80, 255, 0.08),
                transparent 30%
            );
    }


    /* ==============================
       MAIN CONTAINER
    ============================== */

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ==============================
       BUTTONS
    ============================== */

    .stButton > button {
        width: 100%;
        border-radius: 13px;
        min-height: 45px;
        font-weight: 650;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
    }


    /* ==============================
       CHAT
    ============================== */

    [data-testid="stChatMessage"] {
        border-radius: 18px;
        padding: 12px 16px;
        margin-bottom: 12px;
    }


    /* ==============================
       SIDEBAR
    ============================== */

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.15);
    }


    /* ==============================
       INPUT
    ============================== */

    [data-testid="stChatInput"] {
        border-radius: 16px;
    }


    /* ==============================
       AUDIO
    ============================== */

    [data-testid="stAudioInput"] {
        border-radius: 16px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


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
            f"❌ حدث خطأ أثناء تشغيل Gemini:\n\n{error}"
        )

        st.stop()


# ==================================================
# SPEAKER
# ==================================================

if "speaker" not in st.session_state:

    try:

        st.session_state.speaker = Speaker()

    except Exception as error:

        st.warning(
            f"⚠️ نظام الصوت غير متاح:\n\n{error}"
        )

        st.session_state.speaker = None


# ==================================================
# HEADER
# ==================================================

st.title("🤖 CodeBox AI")

st.caption(
    "مساعدك الشخصي للبرمجة والتكنولوجيا والتعلم."
)

st.divider()


# ==================================================
# TOP INFO
# ==================================================

info1, info2, info3 = st.columns(3)


with info1:

    st.metric(
        "🧠 الذكاء",
        "Gemini"
    )


with info2:

    st.metric(
        "🎤 الصوت",
        "متاح" if st.session_state.speaker else "غير متاح"
    )


with info3:

    st.metric(
        "💬 الرسائل",
        len(st.session_state.messages)
    )


st.divider()


# ==================================================
# CHAT HISTORY
# ==================================================

if not st.session_state.messages:

    st.info(
        """
        👋 أهلاً بك في CodeBox AI

        اكتب سؤالك أو استخدم الميكروفون للتحدث مع المساعد.

        يمكنك سؤاله عن:
        - 🐍 Python
        - 💻 البرمجة
        - 🤖 الذكاء الاصطناعي
        - 🐞 حل الأخطاء
        - 📚 التعلم
        """
    )


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ==================================================
# VOICE
# ==================================================

st.divider()

st.subheader("🎤 التحدث مع المساعد")

st.caption(
    "سجّل رسالتك وسيتم تحويل صوتك إلى نص تلقائيًا."
)


audio_value = st.audio_input(
    "🎙️ اضغط هنا للتسجيل"
)


# ==================================================
# VOICE TO TEXT
# ==================================================

voice_text = None


if audio_value is not None:

    try:

        recognizer = sr.Recognizer()

        audio_bytes = audio_value.getvalue()

        audio_file = io.BytesIO(
            audio_bytes
        )

        with sr.AudioFile(audio_file) as source:

            audio_data = recognizer.record(source)

        voice_text = recognizer.recognize_google(
            audio_data,
            language="ar-EG",
        )

        st.success(
            f"🎤 الرسالة: {voice_text}"
        )

    except sr.UnknownValueError:

        st.warning(
            "❓ لم أستطع فهم الصوت."
        )

    except sr.RequestError as error:

        st.error(
            f"❌ خدمة التعرف على الصوت غير متاحة:\n{error}"
        )

    except Exception as error:

        st.error(
            f"❌ حدث خطأ:\n{error}"
        )


# ==================================================
# CHAT INPUT
# ==================================================

prompt = st.chat_input(
    "اكتب رسالتك هنا... 💬"
)


# ==================================================
# SELECT MESSAGE
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

    # Stop previous audio

    if st.session_state.speaker:

        st.session_state.speaker.stop()


    # ----------------------------------------------
    # USER
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )


    with st.chat_message("user"):

        st.write(user_message)


    # ----------------------------------------------
    # AI
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("🤔 CodeBox AI يفكر..."):

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
                    f"❌ حدث خطأ أثناء الحصول على الرد:\n\n"
                    f"{error}"
                )


        st.write(response)


        st.session_state.last_response = response


        # ------------------------------------------
        # SPEAK
        # ------------------------------------------

        if st.session_state.speaker:

            try:

                st.session_state.speaker.speak(
                    response
                )

            except Exception as error:

                st.warning(
                    f"⚠️ تعذر تشغيل الصوت: {error}"
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
# CONTROL PANEL
# ==================================================

st.divider()

st.subheader("🎛️ التحكم")


control1, control2, control3 = st.columns(3)


# ==================================================
# PLAY
# ==================================================

with control1:

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
                "لا يوجد رد صوتي."
            )


# ==================================================
# STOP
# ==================================================

with control2:

    if st.button(
        "🔇 إيقاف الصوت",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            st.session_state.speaker.stop()

            st.toast(
                "🔇 تم إيقاف الصوت"
            )


# ==================================================
# CLEAR
# ==================================================

with control3:

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
            "🗑️ تم مسح المحادثة"
        )

        st.rerun()


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🤖 CodeBox AI")

    st.caption(
        "مساعدك الشخصي للبرمجة والتكنولوجيا."
    )

    st.divider()


    # ----------------------------------------------
    # STATUS
    # ----------------------------------------------

    st.subheader("📊 الحالة")


    if st.session_state.speaker:

        if st.session_state.speaker.is_playing():

            st.warning(
                "🗣️ المساعد يتحدث"
            )

        else:

            st.success(
                "🟢 المساعد جاهز"
            )

    else:

        st.error(
            "🔴 الصوت غير متاح"
        )


    st.divider()


    # ----------------------------------------------
    # QUICK ACTIONS
    # ----------------------------------------------

    st.subheader("⚡ تحكم سريع")


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


    # ----------------------------------------------
    # INFORMATION
    # ----------------------------------------------

    st.subheader("ℹ️ معلومات")

    st.write(
        "🎤 التعرف على الصوت"
    )

    st.write(
        "🔊 تحويل النص إلى كلام"
    )

    st.write(
        "🧠 Gemini AI"
    )

    st.write(
        "🐍 Python"
    )

    st.write(
        "🚀 CodeBox"
    )
