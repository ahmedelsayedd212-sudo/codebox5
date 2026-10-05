import streamlit as st

from utils.python_tools import (
    count_lines,
    count_functions,
    count_classes,
    find_imports,
    check_keywords
)


st.title("🐍 Python Tools")

st.write(
    "مجموعة أدوات تساعدك على تحليل كود Python."
)


code = st.text_area(
    "ضع كود Python هنا:",
    height=350,
    placeholder="""def hello():
    print("Hello Ahmed")

hello()
"""
)


if st.button("🔍 Analyze Python Code", type="primary"):

    if not code.strip():

        st.warning("اكتب كود Python أولاً.")

    else:

        # ==========================
        # Statistics
        # ==========================

        st.subheader("📊 Code Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📝 Lines",
                count_lines(code)
            )

        with col2:
            st.metric(
                "🔧 Functions",
                count_functions(code)
            )

        with col3:
            st.metric(
                "📦 Classes",
                count_classes(code)
            )


        st.divider()


        # ==========================
        # Imports
        # ==========================

        st.subheader("📦 Imports")

        imports = find_imports(code)

        if imports:

            for item in imports:
                st.code(item)

        else:

            st.info("لم يتم العثور على Imports.")


        st.divider()


        # ==========================
        # Keywords
        # ==========================

        st.subheader("🔑 Python Keywords")

        keywords = check_keywords(code)

        if keywords:

            st.write(
                ", ".join(keywords)
            )

        else:

            st.info(
                "لم يتم العثور على Keywords."
            )