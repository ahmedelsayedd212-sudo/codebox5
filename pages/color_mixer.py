import streamlit as st


# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="Color Mixer | CodeBox",
    page_icon="🎨",
    layout="wide",
)


# ==========================================
# CSS
# ==========================================

st.markdown(
    """
    <style>

    .title {
        font-size: 45px;
        font-weight: 800;
        text-align: center;
    }

    .subtitle {
        text-align: center;
        font-size: 19px;
        opacity: 0.75;
        margin-bottom: 30px;
    }

    .result-title {
        text-align: center;
        font-size: 28px;
        font-weight: 700;
    }

    .color-box {
        height: 220px;
        border-radius: 20px;
        margin: 20px 0;
        border: 2px solid rgba(128,128,128,0.3);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# Header
# ==========================================

st.markdown(
    '<div class="title">🎨 Color Mixer</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'اختر لونين وشوف اللون الناتج من دمجهم 🚀'
    '</div>',
    unsafe_allow_html=True,
)

st.divider()


# ==========================================
# Color Pickers
# ==========================================

col1, col2 = st.columns(2)


with col1:

    st.write("### 🎨 اللون الأول")

    color1 = st.color_picker(
        "اختار اللون الأول",
        "#FF0000",
    )


with col2:

    st.write("### 🎨 اللون الثاني")

    color2 = st.color_picker(
        "اختار اللون الثاني",
        "#0000FF",
    )


st.divider()


# ==========================================
# Mix Button
# ==========================================

if st.button(
    "🎨 دمج اللونين",
    use_container_width=True,
    type="primary",
):

    # --------------------------------------
    # HEX → RGB
    # --------------------------------------

    r1 = int(color1[1:3], 16)
    g1 = int(color1[3:5], 16)
    b1 = int(color1[5:7], 16)

    r2 = int(color2[1:3], 16)
    g2 = int(color2[3:5], 16)
    b2 = int(color2[5:7], 16)


    # --------------------------------------
    # Mix RGB
    # --------------------------------------

    r = round((r1 + r2) / 2)
    g = round((g1 + g2) / 2)
    b = round((b1 + b2) / 2)


    # --------------------------------------
    # RGB → HEX
    # --------------------------------------

    result = f"#{r:02X}{g:02X}{b:02X}"


    # ======================================
    # Result
    # ======================================

    st.write("")

    st.markdown(
        '<div class="result-title">'
        '✨ اللون الناتج'
        '</div>',
        unsafe_allow_html=True,
    )


    # Color preview

    st.markdown(
        f"""
        <div class="color-box"
             style="background-color: {result};">
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ======================================
    # Color Information
    # ======================================

    info1, info2 = st.columns(2)


    with info1:

        st.write("### 🔢 HEX")

        st.code(
            result,
            language="text",
        )


    with info2:

        st.write("### 📊 RGB")

        st.code(
            f"rgb({r}, {g}, {b})",
            language="css",
        )


    # ======================================
    # CSS Code
    # ======================================

    st.write("### 💻 CSS")

    st.code(
        f"""color: {result};""",
        language="css",
    )

    st.success(
        f"تم دمج {color1} + {color2} → {result} 🎉"
    )