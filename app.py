```python
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
# CSS ONLY
# ==================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(
                circle at top left,
                rgba(80, 110, 255, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at bottom right,
                rgba(160, 80, 255, 0.10),
                transparent 30%
            );
    }

    /* Main container */
    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 14px;
        min-height: 48px;
        font-size: 15px;
        font-weight: 700;
        border: 1px solid rgba(120, 130, 255, 0.25);
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: rgba(120, 130, 255, 0.7);
        box-shadow: 0 8px 25px rgba(80, 90, 180, 0.15);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.15);
    }

    /* Divider */
    hr {
        opacity: 0.15;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# HEADER
# ==================================================

st.title("💻 CodeBox")

st.caption(
    "⚡ مجموعة أدوات ذكية للمبرمجين والمستخدمين في مكان واحد"
)

st.divider()


# ==================================================
# WELCOME
# ==================================================

st.header("👋 أهلاً بك في CodeBox")

st.info(
    """
    🚀 CodeBox هو مكان واحد يجمع أدوات مفيدة
    للبرمجة والذكاء الاصطناعي والنصوص والألوان
    والعديد من الأدوات اليومية.
    """
)


# ==================================================
# TOOLS
# ==================================================

st.subheader("🧰 الأدوات")

st.write("اختر الأداة التي تريد استخدامها:")

col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("🤖 AI Assistant")

    st.write(
        "مساعد ذكي يساعدك في البرمجة "
        "والأسئلة التقنية."
    )

    if st.button("فتح المساعد", key="ai"):
        st.success("تم اختيار AI Assistant")


with col2:

    st.subheader("🧮 Calculator")

    st.write(
        "آلة حاسبة سريعة للعمليات "
        "الحسابية."
    )

    if st.button("فتح الحاسبة", key="calculator"):
        st.success("تم اختيار Calculator")


with col3:

    st.subheader("🎨 Color Tools")

    st.write(
        "أدوات للتعامل مع الألوان "
        "واختيارها."
    )

    if st.button("فتح الألوان", key="colors"):
        st.success("تم اختيار Color Tools")


# ==================================================
# SECOND ROW
# ==================================================

st.write("")

col4, col5, col6 = st.columns(3)


with col4:

    st.subheader("📝 Text Tools")

    st.write(
        "أدوات لمعالجة النصوص "
        "وتنظيمها."
    )

    if st.button("فتح أدوات النصوص", key="text"):
        st.success("تم اختيار Text Tools")


with col5:

    st.subheader("🐍 Python Tools")

    st.write(
        "أدوات مفيدة للمبرمجين "
        "ومشاريع Python."
    )

    if st.button("فتح Python Tools", key="python"):
        st.success("تم اختيار Python Tools")


with col6:

    st.subheader("🔐 Security")

    st.write(
        "أدوات بسيطة لبعض مهام "
        "الأمان والحماية."
    )

    if st.button("فتح Security", key="security"):
        st.success("تم اختيار Security")


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "💻 CodeBox • Code smarter. Build faster. ⚡"
)
```
