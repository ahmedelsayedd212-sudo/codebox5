import streamlit as st

from utils.converter import (
    km_to_miles,
    miles_to_km,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    kg_to_pounds,
    pounds_to_kg
)


st.title("🔄 Unit Converter")

st.write("حوّل بين الوحدات بسهولة 🚀")


conversion = st.selectbox(
    "اختر نوع التحويل",
    [
        "كيلومتر → ميل",
        "ميل → كيلومتر",
        "درجة مئوية → فهرنهايت",
        "فهرنهايت → درجة مئوية",
        "كيلوجرام → رطل",
        "رطل → كيلوجرام"
    ]
)


value = st.number_input(
    "أدخل القيمة",
    value=0.0
)


if st.button("تحويل 🔄"):

    if conversion == "كيلومتر → ميل":
        result = km_to_miles(value)

    elif conversion == "ميل → كيلومتر":
        result = miles_to_km(value)

    elif conversion == "درجة مئوية → فهرنهايت":
        result = celsius_to_fahrenheit(value)

    elif conversion == "فهرنهايت → درجة مئوية":
        result = fahrenheit_to_celsius(value)

    elif conversion == "كيلوجرام → رطل":
        result = kg_to_pounds(value)

    else:
        result = pounds_to_kg(value)

    st.success(f"النتيجة = {result:.2f}")