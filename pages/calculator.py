import streamlit as st
from utils.calculator import calculate


st.title("🧮 Calculator")
st.write("حاسبة بسيطة وسريعة داخل CodeBox")


num1 = st.number_input(
    "الرقم الأول",
    value=0
)

operator = st.selectbox(
    "اختر العملية",
    ["+", "-", "*", "/"]
)

num2 = st.number_input(
    "الرقم الثاني",
    value=0
)


if st.button("احسب 🚀"):
    try:
        result = calculate(num1, operator, num2)

        st.success(f"النتيجة = {result}")

    except ValueError as error:
        st.error(str(error))