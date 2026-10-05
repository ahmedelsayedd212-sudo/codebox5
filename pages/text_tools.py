import streamlit as st

from utils.text_tools import (
    count_words,
    count_characters,
    reverse_text,
    remove_extra_spaces,
    to_uppercase,
    to_lowercase
)


st.title("📝 Text Tools")

st.write("مجموعة أدوات بسيطة للتعامل مع النصوص 🚀")


text = st.text_area(
    "اكتب النص هنا:",
    height=200
)


tool = st.selectbox(
    "اختر الأداة:",
    [
        "عدد الكلمات",
        "عدد الحروف",
        "عكس النص",
        "إزالة المسافات الزائدة",
        "تحويل إلى حروف كبيرة",
        "تحويل إلى حروف صغيرة"
    ]
)


if st.button("تنفيذ 🚀"):

    if not text.strip():
        st.warning("اكتب نصًا أولاً.")
    
    elif tool == "عدد الكلمات":
        st.success(f"عدد الكلمات: {count_words(text)}")

    elif tool == "عدد الحروف":
        st.success(f"عدد الحروف: {count_characters(text)}")

    elif tool == "عكس النص":
        st.code(reverse_text(text))

    elif tool == "إزالة المسافات الزائدة":
        st.code(remove_extra_spaces(text))

    elif tool == "تحويل إلى حروف كبيرة":
        st.code(to_uppercase(text))

    elif tool == "تحويل إلى حروف صغيرة":
        st.code(to_lowercase(text))