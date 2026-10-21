
import streamlit as st

st.set_page_config(page_title="CodeBox Test", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #07110d;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background:#102d24;
    color:white;
    padding:35px;
    border-radius:20px;
    border:1px solid #34d399;
">
    <h1>أهلاً بك في <span style="color:#34d399">CodeBox</span></h1>
    <p>لو الكلام ده ظهر بتصميم أخضر، يبقى عرض HTML شغال.</p>
</div>
""", unsafe_allow_html=True)
