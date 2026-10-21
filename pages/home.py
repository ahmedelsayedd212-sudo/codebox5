
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CodeBox | Home",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS DESIGN
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at top right, #103c2b 0%, transparent 38%),
        radial-gradient(ellipse at bottom left, #10213c 0%, transparent 35%),
        #070b10;
    color: #f1f5f9;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

#MainMenu, footer {
    visibility: hidden;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 48px 30px;
    border: 1px solid rgba(52, 211, 153, 0.28);
    border-radius: 25px;
    background: linear-gradient(135deg,
        rgba(16, 45, 36, 0.96),
        rgba(10, 20, 32, 0.97));
    box-shadow: 0 15px 55px rgba(0, 0, 0, 0.24);
    animation: fadeIn 1s ease;
}

.hero::before {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    top: -120px;
    right: -70px;
    background: rgba(52, 211, 153, 0.12);
    filter: blur(8px);
}

.logo {
    color: #34d399;
    font-size: 19px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero h1 {
    font-size: clamp(35px, 5vw, 58px);
    font-weight: 800;
    margin: 18px 0 10px 0;
    color: #ffffff;
    line-height: 1.35;
}

.hero h1 span {
    color: #34d399;
}

.hero p {
    color: #cbd5e1;
    font-size: 17px;
    line-height: 2;
    max-width: 700px;
}

.tag {
    display: inline-block;
    padding: 6px 13px;
    border-radius: 30px;
    border: 1px solid rgba(52, 211, 153, 0.35);
    color: #6ee7b7;
    background: rgba(52, 211, 153, 0.08);
    font-size: 13px;
}

.terminal {
    margin-top: 25px;
    padding: 22px;
    border-radius: 16px;
    background: #060a0f;
    border: 1px solid #253746;
    direction: ltr;
    text-align: left;
    color: #d1fae5;
    font-family: Consolas, monospace;
    line-height: 2;
    box-shadow: inset 0 0 25px rgba(52, 211, 153, 0.04);
}

.terminal .muted {
    color: #64748b;
}

.terminal .green {
    color: #34d399;
}

.section-title {
    font-size: 27px;
    font-weight: 800;
    margin: 35px 0 6px 0;
    color: #f8fafc;
}

.section-subtitle {
    color: #94a3b8;
    margin-bottom: 20px;
}

.feature-card {
    min-height: 175px;
    padding: 22px;
    border-radius: 18px;
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid #263449;
    transition: all 0.25s ease;
    margin-bottom: 12px;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: #34d399;
    box-shadow: 0 10px 30px rgba(52, 211, 153, 0.08);
}

.feature-icon {
    font-size: 30px;
    margin-bottom: 12px;
}

.feature-card h3 {
    color: #f1f5f9;
    font-size: 18px;
    margin: 0 0 8px 0;
}

.feature-card p {
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.9;
    margin: 0;
}

.footer-box {
    text-align: center;
    margin-top: 35px;
    padding: 20px;
    border-top: 1px solid #263449;
    color: #64748b;
    font-size: 13px;
}

div.stButton > button {
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
    border: 1px solid #34d399;
    background: #34d399;
    color: #07110d;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background: #6ee7b7;
    border-color: #6ee7b7;
    transform: translateY(-2px);
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
""", unsafe_allow_html=True)


# =========================
# WELCOME ANIMATION
# =========================
if "codebox_welcome_shown" not in st.session_state:
    st.session_state.codebox_welcome_shown = True

    components.html("""
    <div style="
        position:fixed;
        inset:0;
        z-index:999999;
        background:#070b10;
        color:#f8fafc;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        font-family:Arial,sans-serif;
        animation: hideScreen 3.2s forwards;
    ">
        <div style="
            width:82px;
            height:82px;
            border:2px solid #34d399;
            border-radius:22px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:37px;
            box-shadow:0 0 35px rgba(52,211,153,.22);
            animation: logoPop .8s ease;
        ">💻</div>

        <h1 style="margin:22px 0 5px;font-size:37px;letter-spacing:2px">
            Code<span style="color:#34d399">Box</span>
        </h1>

        <p style="color:#94a3b8;font-size:14px">
            YOUR CODING SPACE
        </p>

        <div style="
            width:180px;
            height:3px;
            background:#1e293b;
            border-radius:10px;
            overflow:hidden;
            margin-top:25px;
        ">
            <div style="
                height:100%;
                width:0;
                background:#34d399;
                animation: loadBar 2.2s ease forwards;
            "></div>
        </div>

        <style>
            @keyframes loadBar {
                to { width:100%; }
            }
            @keyframes logoPop {
                from { opacity:0; transform:scale(.6); }
                to { opacity:1; transform:scale(1); }
            }
            @keyframes hideScreen {
                0%, 75% { opacity:1; visibility:visible; }
                100% { opacity:0; visibility:hidden; pointer-events:none; }
            }
        </style>
    </div>
    """, height=0)


# =========================
# HERO SECTION
# =========================
st.markdown("""
<div class="hero">
    <div class="logo">💻 CODEBOX</div>
    <div style="margin-top:18px">
        <span class="tag">🚀 YOUR DEVELOPER TOOLKIT</span>
    </div>

    <h1>
        أهلاً بك في <span>CodeBox</span>
    </h1>

    <p>
        مساحة واحدة تجمع أدواتك البرمجية في مكان واحد.
        نظّم شغلك، جرّب أفكارك، واستخدم أدوات تساعدك
        في رحلة تعلّم البرمجة وتطوير مشاريعك.
    </p>

    <div class="terminal">
        <div class="muted">// Welcome to your workspace</div>
        <div><span class="green">const</span> developer = "You";</div>
        <div><span class="green">const</span> workspace = "CodeBox";</div>
        <div style="margin-top:8px">
            <span class="green">print</span>("Let's build something great!")
        </div>
        <div class="green" style="margin-top:8px">
            &gt; Ready to code_ 
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# TOOLS SECTION
# =========================
st.markdown("""
<div class="section-title">🧰 أدواتك البرمجية</div>
<div class="section-subtitle">
كل اللي تحتاجه في مكان واحد، بسهولة وسرعة.
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧮</div>
        <h3>Calculator</h3>
        <p>إجراء العمليات الحسابية بطريقة سهلة وسريعة.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔄</div>
        <h3>Converter</h3>
        <p>تحويل القيم والوحدات حسب احتياجاتك.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔐</div>
        <h3>Password Generator</h3>
        <p>إنشاء كلمات مرور قوية لحساباتك.</p>
    </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🐍</div>
        <h3>Python Tools</h3>
        <p>أدوات تساعدك أثناء كتابة وتجربة أكواد Python.</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📝</div>
        <h3>Text Tools</h3>
        <p>تنسيق النصوص والتعامل معها بسهولة.</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <h3>CodeBox AI</h3>
        <p>مساعد ذكي لدعمك في البرمجة وحل المشكلات.</p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# STATUS
# =========================
st.markdown('<div class="section-title">📊 حالة المنصة</div>',
            unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("🧮 Calculator", "متاحة")

with m2:
    st.metric("🔄 Converter", "متاحة")

with m3:
    st.metric("🔐 Password", "متاحة")


st.divider()

st.info(
    "💡 اختار الأداة اللي محتاجها من القائمة الجانبية لبدء الاستخدام."
)

st.markdown("""
<div class="footer-box">
    <div style="color:#34d399;font-weight:800;font-size:17px">
        💻 CodeBox
    </div>
    Built for developers, learners, and creators.
    <br>
    © CodeBox — Keep Learning. Keep Building.
</div>
""", unsafe_allow_html=True)
