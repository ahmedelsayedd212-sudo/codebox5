import streamlit as st
from datetime import datetime, timezone
import string

from utils.json_tools import format_json, validate_json


# =========================================================
# العنوان
# =========================================================

st.title("🔧 أدوات المطورين")

st.write("أدوات مفيدة للمبرمجين 👨‍💻")


# =========================================================
# 1️⃣ أدوات JSON
# =========================================================

st.header("📋 أدوات JSON")

json_text = st.text_area(
    "ضع JSON هنا:",
    height=250,
    placeholder='{"name": "Ahmed", "age": 14}'
)

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ فحص JSON", use_container_width=True):
        if validate_json(json_text):
            st.success("JSON صحيح ✅")
        else:
            st.error("JSON غير صحيح ❌")

with col2:
    if st.button("✨ تنسيق JSON", use_container_width=True):
        try:
            formatted = format_json(json_text)
            st.code(formatted, language="json")

        except ValueError:
            st.error("الـ JSON غير صحيح ❌")


st.divider()




# =========================================================
# 4️⃣ 🔢 محوّل أنظمة الأرقام
# =========================================================

st.header("🔢 محوّل أنظمة الأرقام")

number = st.text_input(
    "أدخل الرقم:",
    placeholder="مثال: 255"
)


number_base = st.selectbox(
    "النظام الحالي:",
    [2, 8, 10, 16],

    format_func=lambda base: {

        2: "🔵 ثنائي (Binary)",

        8: "🟢 ثماني (Octal)",

        10: "🟡 عشري (Decimal)",

        16: "🟣 سداسي عشر (Hexadecimal)"

    }[base]
)


if st.button(
    "🔄 تحويل الرقم",
    use_container_width=True
):

    if not number.strip():

        st.warning("⚠️ أدخل رقمًا أولًا.")

    else:

        try:

            value = int(
                number.strip(),
                number_base
            )

            st.success(
                "تم التحويل بنجاح ✅"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write("### الأنظمة")

                st.write(
                    f"🔵 **ثنائي:** `{bin(value)[2:]}`"
                )

                st.write(
                    f"🟢 **ثماني:** `{oct(value)[2:]}`"
                )

            with col2:

                st.write("### الأنظمة")

                st.write(
                    f"🟡 **عشري:** `{value}`"
                )

                st.write(
                    f"🟣 **سداسي عشر:** "
                    f"`{hex(value)[2:].upper()}`"
                )

        except ValueError:

            st.error(
                "❌ الرقم لا يتوافق مع النظام المختار."
            )