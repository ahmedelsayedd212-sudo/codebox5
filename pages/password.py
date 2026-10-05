import streamlit as st

from utils.password import generate_password


st.title("🔐 Password Generator")

st.write("أنشئ كلمة مرور عشوائية وقوية بسهولة.")


length = st.slider(
    "طول كلمة المرور",
    min_value=6,
    max_value=50,
    value=12
)

use_numbers = st.checkbox(
    "إضافة أرقام 🔢",
    value=True
)

use_symbols = st.checkbox(
    "إضافة رموز 🔣",
    value=True
)


if st.button("إنشاء كلمة مرور 🚀"):

    password = generate_password(
        length,
        use_numbers,
        use_symbols
    )

    st.code(password)

    st.success("تم إنشاء كلمة المرور بنجاح!")