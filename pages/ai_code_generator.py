import streamlit as st

from utils.gemini_ai import GeminiAI


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title=" Ahmed AI  | CodeBox",
    page_icon="🧑‍💻",
    layout="wide",
)


# ==================================================
# CSS
# ==================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 46px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 19px;
        opacity: 0.75;
        margin-bottom: 30px;
    }

    .feature-card {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.25);
        min-height: 130px;
        margin-bottom: 15px;
    }

    .feature-title {
        font-size: 20px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">👨‍💻AHMED AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'اكتب فكرتك، أنشئ الكود، عدّله، افحصه واشرحه 🚀'
    '</div>',
    unsafe_allow_html=True,
)

st.divider()


# ==================================================
# AI INITIALIZATION
# ==================================================

if "code_ai" not in st.session_state:

    try:
        st.session_state.code_ai = GeminiAI()

    except Exception as error:

        st.error(
            f"حدث خطأ أثناء تشغيل Gemini:\n\n{error}"
        )

        st.stop()


ai = st.session_state.code_ai


# ==================================================
# SESSION STATE
# ==================================================

if "generated_code" not in st.session_state:
    st.session_state.generated_code = ""

if "generated_language" not in st.session_state:
    st.session_state.generated_language = "Python"

if "project_name" not in st.session_state:
    st.session_state.project_name = "my_project"

if "saved_projects" not in st.session_state:
    st.session_state.saved_projects = {}


# ==================================================
# SETTINGS
# ==================================================

st.write("## ⚙️ إعدادات المشروع")

col1, col2, col3 = st.columns(3)


with col1:

    language = st.selectbox(
        "💻 لغة البرمجة",
        [
            "Python",
            "JavaScript",
            "HTML",
            "CSS",
            "Java",
            "C++",
            "C#",
            "TypeScript",
            "PHP",
            "SQL",
        ],
    )


with col2:

    level = st.selectbox(
        "📚 مستوى المشروع",
        [
            "مبتدئ",
            "متوسط",
            "متقدم",
        ],
    )


with col3:

    project_name = st.text_input(
        "📁 اسم المشروع",
        value="my_project",
    )


# ==================================================
# REQUEST
# ==================================================

st.write("## 💡 ماذا تريد أن تبني؟")

request = st.text_area(
    "وصف المشروع",
    height=160,
    placeholder=(
        "مثال:\n"
        "اعمل برنامج Java لإدارة الطلاب. "
        "أريد إضافة طالب وحذفه والبحث عنه "
        "وحساب متوسط درجات الطلاب."
    ),
)


# ==================================================
# GENERATE CODE
# ==================================================

if st.button(
    "🚀 إنشاء الكود",
    type="primary",
    use_container_width=True,
):

    if not request.strip():

        st.warning(
            "⚠️ اكتب وصف المشروع أولًا."
        )

    else:

        prompt = f"""
أنت مبرمج محترف.

أنشئ مشروعًا كاملًا بناءً على طلب المستخدم.

لغة البرمجة:
{language}

المستوى:
{level}

اسم المشروع:
{project_name}

طلب المستخدم:
{request}

القواعد:

1. اكتب كودًا كاملًا وقابلًا للتشغيل.
2. استخدم أفضل الممارسات.
3. اجعل الكود منظمًا وواضحًا.
4. ضع الكود داخل Markdown code block.
5. لا تخترع مكتبات غير موجودة.
6. إذا كان المشروع يحتاج عدة ملفات، وضح أسماء الملفات.
7. أضف تعليقات مفيدة داخل الكود.
"""

        with st.spinner(
            "🤖 Gemini يقوم بإنشاء المشروع..."
        ):

            result = ai.generate_response(
                prompt
            )

        st.session_state.generated_code = result
        st.session_state.generated_language = language
        st.session_state.project_name = project_name

        st.success(
            "✅ تم إنشاء المشروع!"
        )


# ==================================================
# GENERATED CODE
# ==================================================

if st.session_state.generated_code:

    st.divider()

    st.write("## 💻 الكود الناتج")

    edited_code = st.text_area(
        "يمكنك تعديل الكود مباشرة:",
        value=st.session_state.generated_code,
        height=450,
    )

    st.session_state.generated_code = edited_code


    # ==================================================
    # ACTION BUTTONS
    # ==================================================

    st.write("### 🛠️ أدوات الكود")

    c1, c2, c3 = st.columns(3)


    # ==================================================
    # EXPLAIN
    # ==================================================

    with c1:

        if st.button(
            "📚 شرح الكود",
            use_container_width=True,
        ):

            prompt = f"""
اشرح الكود التالي بطريقة بسيطة جدًا.

لغة البرمجة:
{language}

الكود:

{st.session_state.generated_code}

اشرح:
- وظيفة البرنامج
- أهم الأجزاء
- أهم الدوال
- كيف يعمل البرنامج
"""

            with st.spinner(
                "📚 جاري شرح الكود..."
            ):

                explanation = ai.generate_response(
                    prompt
                )

            st.session_state.code_explanation = (
                explanation
            )


    # ==================================================
    # FIND BUGS
    # ==================================================

    with c2:

        if st.button(
            "🐞 فحص الأخطاء",
            use_container_width=True,
        ):

            prompt = f"""
افحص الكود التالي بحثًا عن الأخطاء.

لغة البرمجة:
{language}

الكود:

{st.session_state.generated_code}

أريد:
1. تحديد الأخطاء.
2. شرح سبب الخطأ.
3. تقديم الحل.
4. كتابة النسخة المصححة إذا لزم الأمر.
"""

            with st.spinner(
                "🔍 جاري فحص الكود..."
            ):

                bugs = ai.generate_response(
                    prompt
                )

            st.session_state.code_bugs = bugs


    # ==================================================
    # IMPROVE
    # ==================================================

    with c3:

        if st.button(
            "✨ تحسين الكود",
            use_container_width=True,
        ):

            prompt = f"""
حسّن الكود التالي.

لغة البرمجة:
{language}

الكود:

{st.session_state.generated_code}

المطلوب:

- تحسين التنظيم.
- تقليل التكرار.
- تحسين الأداء عند الحاجة.
- تحسين أسماء المتغيرات.
- الحفاظ على نفس الوظيفة.
- أعطني الكود المحسن كاملًا.
"""

            with st.spinner(
                "✨ جاري تحسين الكود..."
            ):

                improved = ai.generate_response(
                    prompt
                )

            st.session_state.generated_code = (
                improved
            )

            st.rerun()


    # ==================================================
    # RESULTS
    # ==================================================

    if "code_explanation" in st.session_state:

        st.divider()

        st.write("## 📚 شرح الكود")

        st.markdown(
            st.session_state.code_explanation
        )


    if "code_bugs" in st.session_state:

        st.divider()

        st.write("## 🐞 نتيجة فحص الأخطاء")

        st.markdown(
            st.session_state.code_bugs
        )


    # ==================================================
    # DOWNLOAD
    # ==================================================

    extension_map = {
        "Python": "py",
        "JavaScript": "js",
        "HTML": "html",
        "CSS": "css",
        "Java": "java",
        "C++": "cpp",
        "C#": "cs",
        "TypeScript": "ts",
        "PHP": "php",
        "SQL": "sql",
    }

    extension = extension_map.get(
        language,
        "txt",
    )


    st.divider()

    st.download_button(
        "📥 تحميل الكود",
        data=st.session_state.generated_code,
        file_name=(
            f"{st.session_state.project_name}"
            f".{extension}"
        ),
        mime="text/plain",
        use_container_width=True,
    )


    # ==================================================
    # SAVE PROJECT
    # ==================================================

    st.write("## 💾 حفظ المشروع")

    if st.button(
        "💾 حفظ المشروع",
        use_container_width=True,
    ):

        st.session_state.saved_projects[
            project_name
        ] = {
            "language": language,
            "code": st.session_state.generated_code,
        }

        st.success(
            f"✅ تم حفظ مشروع {project_name}"
        )


# ==================================================
# SAVED PROJECTS
# ==================================================

if st.session_state.saved_projects:

    st.divider()

    st.write("## 📁 المشاريع المحفوظة")

    for name, project in (
        st.session_state.saved_projects.items()
    ):

        with st.expander(
            f"📁 {name}"
        ):

            st.write(
                f"💻 اللغة: {project['language']}"
            )

            st.code(
                project["code"],
                language=(
                    project["language"].lower()
                ),
            )


# ==================================================
# NEW PROJECT
# ==================================================

st.divider()

if st.button(
    "🔄 مشروع جديد",
    use_container_width=True,
):

    st.session_state.generated_code = ""

    st.session_state.pop(
        "code_explanation",
        None,
    )

    st.session_state.pop(
        "code_bugs",
        None,
    )

    st.rerun()


# ==================================================
# FEATURES
# ==================================================

st.divider()

st.write("## ✨ مميزات AI Code Studio")

f1, f2, f3, f4 = st.columns(4)


with f1:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        🤖 Generate
        </div>

        إنشاء كود من وصف بسيط.

        </div>
        """,
        unsafe_allow_html=True,
    )


with f2:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        🐞 Debug
        </div>

        اكتشاف الأخطاء والمساعدة في إصلاحها.

        </div>
        """,
        unsafe_allow_html=True,
    )


with f3:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        📚 Explain
        </div>

        شرح الكود بطريقة بسيطة.

        </div>
        """,
        unsafe_allow_html=True,
    )


with f4:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-title">
        ✨ Improve
        </div>

        تحسين وتنظيم الكود.

        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "🤖 CodeBox AI Code Studio — Powered by Gemini"
)