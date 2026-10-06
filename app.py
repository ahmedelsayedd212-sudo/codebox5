import streamlit as st 


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="CodeBox",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# CSS
# ==================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 52px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        opacity: 0.75;
        margin-bottom: 35px;
    }

    .welcome-box {
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 25px;
    }

    .tool-card {
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 20px;
        min-height: 155px;
    }

    .tool-title {
        font-size: 25px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .tool-description {
        font-size: 16px;
        opacity: 0.75;
    }

    .section-title {
        font-size: 30px;
        font-weight: 750;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">💻 CodeBox</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'مجموعة أدوات ذكية للمبرمجين والمستخدمين في مكان واحد 🚀'
    '</div>',
    unsafe_allow_html=True,
)

st.divider()


# ==================================================
# WELCOME
# ==================================================

st.markdown(
    '<div class="section-title">👋 أهلاً بك في CodeBox</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="welcome-box">

    <h3>🚀 CodeBox</h3>

    <p>
    CodeBox عبارة عن مجموعة أدوات مفيدة للمبرمجين
    والمستخدمين في مكان واحد.
    </p>

    <p>
    يمكنك استخدام أدوات البرمجة، الذكاء الاصطناعي،
    الألوان، النصوص والمزيد.
    </p>

    </div>
    """,
    unsafe_allow_html=True,
)
