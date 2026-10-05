import io

import streamlit as st
import speech_recognition as sr

from utils.gemini_ai import GeminiAI
from utils.speaker import Speaker


# =========================================================
# إعداد الصفحة
# =========================================================

st.set_page_config(
    page_title="CodeBox Personal Assistant",
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
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(124, 58, 237, 0.18),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 15%,
                rgba(6, 182, 212, 0.14),
                transparent 25%
            ),
            radial-gradient(
                circle at 50% 90%,
                rgba(168, 85, 247, 0.10),
                transparent 30%
            );
    }

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        margin-top: 10px;
        margin-bottom: 5px;

        background:
            linear-gradient(
                90deg,
                #7c3aed,
                #06b6d4,
                #8b5cf6
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .main-subtitle {
        text-align: center;
        font-size: 16px;
        opacity: 0.7;
        margin-bottom: 15px;
    }

    .status {
        width: fit-content;
        margin: 0 auto 20px auto;
        padding: 7px 18px;
        border-radius: 50px;

        background:
            linear-gradient(
                135deg,
                rgba(124,58,237,0.15),
                rgba(6,182,212,0.12)
            );

        border:
            1px solid
            rgba(124,58,237,0.35);

        font-size: 13px;
    }

    hr {
        border: none !important;
        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(124,58,237,0.5),
                rgba(6,182,212,0.5),
                transparent
            ) !important;

        margin: 25px 0 !important;
    }

    [data-testid="stChatMessage"] {
        border-radius: 20px;
        padding: 10px 15px;
        margin-top: 10px;
        margin-bottom: 12px;

        border:
            1px solid
            rgba(128,128,128,0.12);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px);

        box-shadow:
            0 8px 25px
            rgba(0,0,0,0.10);
    }

    [data-testid="stChatMessage"] p {
        line-height: 1.9;
        font-size: 15px;
    }

    [data-testid="stChatInput"] {
        margin-top: 15px;
    }

    [data-testid="stChatInput"] textarea {
        border-radius: 18px !important;

        border:
            1px solid
            rgba(124,58,237,0.35) !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color:
            #06b6d4 !important;

        box-shadow:
            0 0 0 2px
            rgba(6,182,212,0.12);
    }

    .stButton > button {
        border-radius: 14px;
        min-height: 44px;
        font-weight: 700;

        border:
            1px solid
            rgba(124,58,237,0.25);

        background:
            linear-gradient(
                135deg,
                rgba(124,58,237,0.10),
                rgba(6,182,212,0.08)
            );
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        border-color:
            rgba(6,182,212,0.65);

        box-shadow:
            0 8px 25px
            rgba(6,182,212,0.15);
    }

    h2,
    h3 {
        background:
            linear-gradient(
                90deg,
                #7c3aed,
                #06b6d4
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        font-weight: 800 !important;
    }

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                rgba(30,20,70,0.98),
                rgba(10,25,45,0.98)
            );

        border-right:
            1px solid
            rgba(124,58,237,0.35);
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    .sidebar-title {
        text-align: center;
        font-size: 28px;
        font-weight: 900;

        background:
            linear-gradient(
                90deg,
                #a78bfa,
                #22d3ee
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sidebar-subtitle {
        text-align: center;
        font-size: 13px;
        opacity: 0.65;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background:
            rgba(255,255,255,0.06);

        border:
            1px solid
            rgba(255,255,255,0.10);

        color: white;
    }

    [data-testid="stAlert"] {
        border-radius: 15px;
    }

    [data-testid="stAudioInput"] {
        border-radius: 18px;
    }

    .app-footer {
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
# Session State
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "assistant" not in st.session_state:
    st.session_state.assistant = None

if "speaker" not in st.session_state:
    st.session_state.speaker = None

if "news_index" not in st.session_state:
    st.session_state.news_index = 0


# =========================================================
# Gemini
# =========================================================

if st.session_state.assistant is None:

    try:
        st.session_state.assistant = GeminiAI()

    except Exception as error:

        st.error("❌ حدث خطأ أثناء تشغيل Gemini.")
        st.code(str(error))
        st.stop()


# =========================================================
# Speaker
# =========================================================

if st.session_state.speaker is None:

    try:
        st.session_state.speaker = Speaker()

    except Exception:
        st.session_state.speaker = None


# =========================================================
# Header
# =========================================================

st.markdown(
    '<div class="main-title">'
    '🤖 CodeBox Personal Assistant'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-subtitle">'
    'مساعدك الشخصي الذكي'
    '</div>',
    unsafe_allow_html=True,
)


# =========================================================
# Status
# =========================================================

if st.session_state.speaker:

    try:
        playing = (
            st.session_state.speaker.is_playing()
        )

    except Exception:
        playing = False

    if playing:

        st.markdown(
            '<div class="status">'
            '🟡 المساعد يتحدث الآن'
            '</div>',
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            '<div class="status">'
            '🟢 المساعد الشخصي جاهز'
            '</div>',
            unsafe_allow_html=True,
        )

else:

    st.markdown(
        '<div class="status">'
        '🟢 المساعد الشخصي جاهز'
        '</div>',
        unsafe_allow_html=True,
    )


st.divider()


# =========================================================
# شريط الأخبار
# =========================================================

if not st.session_state.messages:

    news = [
        "🤖 CodeBox AI جاهز لمساعدتك",
        "💻 اسألني عن البرمجة والتكنولوجيا",
        "🐍 Python • C++ • Java • JavaScript",
        "🧠 Artificial Intelligence",
        "🐞 Debugging وحل مشاكل الكود",
        "🎤 تحدث مع المساعد بالصوت",
        "🔊 المساعد يستطيع الرد عليك صوتيًا",
        "💡 اكتب رسالتك الآن",
    ]

    current_news = news[
        st.session_state.news_index
        % len(news)
    ]

    st.info(
        f"🔴 LIVE  |  {current_news}"
    )

    st.session_state.news_index += 1


# =========================================================
# المحادثة
# =========================================================

for message in st.session_state.messages:

    role = message["role"]

    avatar = (
        "👤"
        if role == "user"
        else "🤖"
    )

    with st.chat_message(
        role,
        avatar=avatar,
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# إدخال الرسائل
# =========================================================

st.subheader("💬 المحادثة")

prompt = st.chat_input(
    "اكتب رسالتك إلى المساعد الشخصي..."
)


# =========================================================
# Voice Input
# =========================================================

st.subheader(
    "🎤 التحدث مع المساعد"
)

st.caption(
    "يمكنك تسجيل رسالة صوتية وسيتم تحويلها إلى نص."
)

audio_value = st.audio_input(
    "🎙️ تسجيل رسالة"
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

        with sr.AudioFile(
            audio_file
        ) as source:

            audio_data = recognizer.record(
                source
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
            "❓ لم أستطع فهم التسجيل."
        )

    except sr.RequestError as error:

        st.error(
            "❌ خدمة التعرف على الصوت غير متاحة."
        )

        st.code(
            str(error)
        )

    except Exception as error:

        st.error(
            "❌ حدث خطأ أثناء معالجة الصوت."
        )

        st.code(
            str(error)
        )


# =========================================================
# اختيار الرسالة
# =========================================================

user_message = None

if voice_text:

    user_message = voice_text

elif prompt:

    user_message = prompt


# =========================================================
# إرسال الرسالة إلى Gemini
# =========================================================

if user_message:

    # إيقاف الصوت القديم
    if st.session_state.speaker:

        try:
            st.session_state.speaker.stop()

        except Exception:
            pass


    # إضافة رسالة المستخدم
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )


    # عرض رسالة المستخدم
    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(
            user_message
        )


    # رد Gemini
    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        with st.spinner(
            "🤖 المساعد الشخصي يفكر..."
        ):

            try:

                response = (
                    st.session_state.assistant
                    .generate_response(
                        user_message
                    )
                )

            except Exception as error:

                response = (
                    "❌ حدث خطأ أثناء الاتصال بـ Gemini.\n\n"
                    + str(error)
                )


        st.markdown(
            response
        )


    # حفظ الرد
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    st.session_state.last_response = response


    # تشغيل الرد صوتيًا
    if st.session_state.speaker:

        try:

            st.session_state.speaker.speak(
                response
            )

        except Exception:
            pass


# =========================================================
# التحكم في الصوت
# =========================================================

st.divider()

st.subheader(
    "🔊 التحكم في الصوت"
)

audio_col1, audio_col2, audio_col3 = (
    st.columns(3)
)


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

                st.code(
                    str(error)
                )

        else:

            st.info(
                "لا يوجد رد لتشغيله."
            )


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

                st.code(
                    str(error)
                )


with audio_col3:

    if st.button(
        "✨ محادثة جديدة",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            try:
                st.session_state.speaker.stop()

            except Exception:
                pass

        st.session_state.messages = []
        st.session_state.last_response = None
        st.session_state.news_index = 0

        try:

            st.session_state.assistant.reset_chat()

        except Exception:
            pass

        st.toast(
            "✨ بدأت محادثة جديدة"
        )

        st.rerun()


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">'
        '🤖 CodeBox AI'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Personal Assistant'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader(
        "📊 حالة المساعد"
    )

    if st.session_state.speaker:

        try:

            playing = (
                st.session_state.speaker
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

    st.subheader(
        "🎛️ التحكم السريع"
    )


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

            except Exception:

                st.error(
                    "❌ حدث خطأ في الصوت."
                )

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

            except Exception:
                pass


    if st.button(
        "✨ محادثة جديدة",
        use_container_width=True,
    ):

        if st.session_state.speaker:

            try:
                st.session_state.speaker.stop()

            except Exception:
                pass

        st.session_state.messages = []
        st.session_state.last_response = None
        st.session_state.news_index = 0

        try:

            st.session_state.assistant.reset_chat()

        except Exception:
            pass

        st.toast(
            "✨ بدأت محادثة جديدة"
        )

        st.rerun()


    st.divider()

    st.subheader(
        "✨ المميزات"
    )

    st.write("💬 محادثة ذكية")
    st.write("🎤 Voice Input")
    st.write("🔊 Voice Response")
    st.write("🧠 Gemini AI")
    st.write("💻 Programming Assistant")
    st.write("🐞 Debugging")
    st.write("📚 Learning Assistant")
    st.write("🌐 عربي + English")

    st.divider()

    st.caption(
        "🚀 CodeBox"
    )

    st.caption(
        "Personal Assistant"
    )

    st.caption(
        "Built with Python + Streamlit"
    )


# =========================================================
# Footer
# =========================================================

st.markdown(
    '<div class="app-footer">'
    '🤖 CodeBox Personal Assistant • Powered by Gemini'
    '</div>',
    unsafe_allow_html=True,
)
