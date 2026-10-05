import streamlit as st


st.title("💻 CodeBox")

st.subheader("كل أدوات البرمجة التي تحتاجها في مكان واحد 🚀")

st.write(
    """
    CodeBox هو مشروع بسيط للمبرمجين والمبتدئين،
    يحتوي على مجموعة من الأدوات المفيدة في مكان واحد.
    """
)


st.divider()


col1, col2, col3 = st.columns(3)


with col1:
    st.metric("🧮 Calculator", "متاحة")


with col2:
    st.metric("🔄 Converter", "متاحة")


with col3:
    st.metric("🔐 Password", "متاحة")


st.divider()


st.info(
    "💡 استخدم القائمة الجانبية للانتقال بين أدوات CodeBox."
)