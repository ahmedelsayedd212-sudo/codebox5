
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CodeBox | Future of Coding",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# SESSION STATE
# =========================

if "codebox_started" not in st.session_state:
    st.session_state.codebox_started = False

# =========================
# FUTURISTIC DESIGN
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Orbitron:wght@500;700;800&display=swap');

:root {
    --green: #00ff88;
    --light-green: #a0ffca;
    --bg: #030805;
    --panel: #09150e;
}

.stApp {
    background:
        radial-gradient(ellipse at 50% 10%,
        #06351d 0%, transparent 42%),
        #030805;
    color: #f4fff7;
    font-family: 'Cairo', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, label {
    font-family: 'Cairo', sans-serif;
}

.hero {
    text-align: center;
    padding: 30px 15px 20px;
    animation: enter 1s ease both;
}

.hero-icon {
    width: 105px;
    height: 105px;
    margin: 0 auto 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--green);
    border-radius: 28px;
    background: linear-gradient(145deg, #103722, #030805);
    color: var(--green);
    font-family: monospace;
    font-size: 42px;
    font-weight: 800;
    box-shadow:
        0 0 25px #00ff8833,
        inset 0 0 25px #00ff8817;
    animation: float 4s ease-in-out infinite;
}

.hero-logo {
    direction: ltr;
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(40px, 7vw, 68px);
    font-weight: 800;
    letter-spacing: -2px;
    color: #f5fff8;
    text-shadow: 0 0 30px #00ff8833;
}

.hero-logo span {
    color: var(--green);
    text-shadow: 0 0 30px #00ff8877;
}

.tagline {
    direction: ltr;
    font-family: monospace;
    color: #90bba1;
    letter-spacing: 3px;
    font-size: 11px;
    margin-top: 8px;
    margin-bottom: 35px;
}

.welcome-title {
    font-size: clamp(25px, 4vw, 39px);
    font-weight: 900;
    margin-bottom: 14px;
}

.welcome-title span {
    color: var(--light-green);
}

.description {
    max-width: 720px;
    margin: auto;
    color: #a9c0b1;
    font-size: 16px;
    line-height: 2.1;
}

.terminal {
    max-width: 680px;
    margin: 25px auto 0;
    padding: 15px 20px;
    direction: ltr;
    text-align: left;
    border: 1px solid #00ff8833;
    border-radius: 12px;
    background: #061109;
    color: var(--green);
    font-family: monospace;
    font-size: 13px;
    box-shadow: 0 0 25px #00ff880b;
}

.terminal small {
    color: #719780;
}

.section-heading {
    color: var(--light-green);
    font-size: 23px;
    font-weight: 800;
    text-align: center;
    margin: 30px 0 20px;
}

.feature-card {
    height: 100%;
    padding: 22px 15px;
    text-align: center;
    background: linear-gradient(145deg, #0b1b11, #07100a);
    border: 1px solid #00ff8827;
    border-radius: 16px;
    transition: all .3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: #00ff88aa;
    box-shadow: 0 10px 30px #00ff8814;
}

.feature-icon {
    font-size: 31px;
    margin-bottom: 8px;
}

.feature-card h3 {
    font-size: 16px;
    color: #f1fff5;
    margin: 5px 0;
}

.feature-card p {
    font-size: 12px;
    color: #8ba895;
    margin-bottom: 0;
}

div.stButton > button {
    border: 1px solid #00ff8877;
    border-radius: 12px;
    background: #0a1b10;
    color: #caffdf;
    min-height: 48px;
    font-family: 'Cairo', sans-serif;
    font-weight: 700;
    transition: all .25s ease;
}

div.stButton > button:hover {
    border-color: var(--green);
    background: #103b22;
    color: white;
    box-shadow: 0 0 20px #00ff8822;
    transform: translateY(-2px);
}

div.stButton > button[kind="primary"] {
    background: var(--green);
    color: #031109;
    border: none;
}

div.stButton > button[kind="primary"]:hover {
    background: #a0ffca;
    box-shadow: 0 0 25px #00ff8855;
}

div[data-testid="stMetric"] {
    padding: 17px;
    border: 1px solid #00ff8827;
    border-radius: 14px;
    background: #09150e;
}

div[data-testid="stMetricLabel"] {
    color: #a9c0b1;
}

div[data-testid="stMetricValue"] {
    color: #00ff88;
    font-family: 'Orbitron', sans-serif;
}

footer {
    visibility: hidden;
}

@keyframes enter {
    from {
        opacity: 0;
        transform: translateY(25px);
        filter: blur(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
        filter: blur(0);
    }
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
, unsafe_allow_html=True)

# =========================
# HERO
# =========================

st.markdown("""
<div class="hero">
    <div class="hero-icon">&lt;/&gt;</div>

    <div class="hero-logo">
        Code<span>Box</span>
    </div>

    <div class="tagline">
        YOUR IDEAS · YOUR CODE · YOUR FUTURE
    </div>

    <div class="welcome-title">
        أهلاً بك في <span>CodeBox</span>
    </div>

    <div class="description">
        مرحباً بك في عالم البرمجة والإبداع!
        <br>
        اجمع أدواتك البرمجية في مكان واحد، واستخدم
        الذكاء الاصطناعي، وطوّر مهاراتك، وحوّل أفكارك
        إلى مشاريع حقيقية.
        <br>
        <span style="color:#00ff88;font-weight:700">
            مستقبلك يبدأ بفكرة... وكود واحد.
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="terminal">
    <div><small>● ● ● &nbsp; CODEBOX TERMINAL</small></div>
    <br>
    <div>&gt; Initializing CodeBox...</div>
    <div>&gt; Developer tools loaded <span style="color:#00ff88">[OK]</span></div>
    <div>&gt; Ready to build something amazing_</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# =========================
# START BUTTON
# =========================

_, center, _ = st.columns([1, 2, 1])

with center:
    if st.button(
        "🚀  لنبدأ الآن",
        type="primary",
        use_container_width=True,
        key="start_codebox",
    ):
        st.session_state.codebox_started = True

if st.session_state.codebox_started:
    st.success("أهلاً بك في مساحة العمل! اختار الأداة اللي عايز تستخدمها من القائمة الجانبية.")
    st.info("استخدم قائمة الصفحات الموجودة في Streamlit للانتقال إلى أدوات CodeBox.")

st.divider()

# =========================
# FEATURES
# =========================

st.markdown( """
    '<div class="section-heading">✦ استكشف عالم CodeBox</div>',
    unsafe_allow_html=True,
)

features = [
    ("🧰", "أدوات المطورين", "أدوات يومية تساعدك في البرمجة."),
    ("🤖", "الذكاء الاصطناعي", "مساعدك الشخصي في كتابة الأكواد."),
    ("🧠", "مولد الأكواد", "حوّل فكرتك إلى كود قابل للتطوير."),
    ("🎨", "الأدوات الإبداعية", "الألوان والتحويلات والأدوات المفيدة."),
]

cols = st.columns(4)

for col, feature in zip(cols, features):
    icon, title, description = feature

    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)

st.write("")
st.divider()

# =========================
# TOOL STATUS
# =========================

st.markdown(
    '<div class="section-heading">⚡ أدواتك في مكان واحد</div>',
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("🧮 Calculator", "جاهزة")

with c2:
    st.metric("🔄 Converter", "جاهزة")

with c3:
    st.metric("🔐 Password", "جاهزة")

st.write("")
st.caption("💚 CodeBox — Built with Python & Streamlit")
