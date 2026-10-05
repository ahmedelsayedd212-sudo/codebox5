import os
import streamlit as st

from google import genai
from google.genai import types


class GeminiAI:
    """Gemini AI client for CodeBox."""

    def __init__(self, api_key=None, model=None):

        # ==========================================
        # API KEY
        # ==========================================

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            try:
                self.api_key = st.secrets.get("GEMINI_API_KEY")
            except Exception:
                self.api_key = None

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set."
            )

        # ==========================================
        # Gemini Client
        # ==========================================

        self.client = genai.Client(
            api_key=self.api_key
        )

        # ==========================================
        # System Instruction
        # ==========================================

        self.system_instruction = """
You are CodeBox Personal Assistant.

You are a friendly and intelligent AI assistant.

You can help with:

- Python
- Java
- C++
- HTML
- CSS
- JavaScript
- TypeScript
- SQL
- Programming
- Debugging
- Programming errors
- Technology
- Studying
- Productivity
- General questions
- Software projects

Rules:

1. Reply in the same language as the user.
2. If the user speaks Arabic, answer in Arabic.
3. If the user speaks English, answer in English.
4. Explain difficult things simply.
5. Use Markdown when useful.
6. Put programming code inside code blocks.
7. Be friendly and helpful.
8. Never claim that you executed code if you did not.
"""

        # ==========================================
        # Get available models
        # ==========================================

        self.models = self._get_available_models()

        # لو المستخدم حدد موديل معين
        if model and model in self.models:
            self.model = model

        elif self.models:
            self.model = self.models[0]

        else:
            raise RuntimeError(
                "لم يتم العثور على أي Gemini model متاح لهذا API Key."
            )

        # ==========================================
        # Create Chat
        # ==========================================

        self.chat_session = self._create_chat(
            self.model
        )

    # ==========================================
    # Get Available Models
    # ==========================================

    def _get_available_models(self):

        available = []

        try:

            for item in self.client.models.list():

                name = getattr(item, "name", "")

                if not name:
                    continue

                # إزالة models/ من الاسم
                if name.startswith("models/"):
                    name = name.replace(
                        "models/",
                        "",
                        1
                    )

                # نريد فقط موديلات Gemini
                if "gemini" not in name.lower():
                    continue

                # نحتاج موديلات تدعم generateContent
                actions = getattr(
                    item,
                    "supported_actions",
                    []
                )

                if actions:

                    actions_text = str(actions).lower()

                    if (
                        "generatecontent"
                        not in actions_text
                        and "generate_content"
                        not in actions_text
                    ):
                        continue

                available.append(name)

        except Exception as error:

            print(
                "Model discovery error:",
                error
            )

        # ==========================================
        # ترتيب الموديلات
        # ==========================================

        preferred = [
            "gemini-3.5-flash",
            "gemini-3.1-flash-lite",
            "gemini-3-flash",
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash",
        ]

        ordered = []

        for model in preferred:

            if model in available:
                ordered.append(model)

        # إضافة أي موديلات أخرى
        for model in available:

            if model not in ordered:
                ordered.append(model)

        return ordered

    # ==========================================
    # Create Chat
    # ==========================================

    def _create_chat(self, model):

        return self.client.chats.create(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                max_output_tokens=4096,
            ),
        )

    # ==========================================
    # Generate Response
    # ==========================================

    def generate_response(self, prompt):

        if not prompt or not prompt.strip():

            return (
                "من فضلك اكتب رسالتك أولاً."
            )

        prompt = prompt.strip()

        last_error = None

        # ==========================================
        # Try available models
        # ==========================================

        for model in self.models:

            try:

                # إنشاء Chat جديد للموديل
                if model != self.model:

                    self.model = model

                    self.chat_session = (
                        self._create_chat(model)
                    )

                response = (
                    self.chat_session
                    .send_message(prompt)
                )

                text = getattr(
                    response,
                    "text",
                    None
                )

                if text:

                    return text.strip()

                return (
                    "Gemini أرسل استجابة بدون نص."
                )

            except Exception as error:

                last_error = error

                error_text = str(
                    error
                ).lower()

                # ==================================
                # Try next model
                # ==================================

                retry_errors = [
                    "404",
                    "not found",
                    "429",
                    "quota",
                    "resource_exhausted",
                    "503",
                    "unavailable",
                    "high demand",
                    "capacity",
                ]

                should_retry = any(
                    word in error_text
                    for word in retry_errors
                )

                if should_retry:

                    continue

                return self._handle_error(
                    error
                )

        # ==========================================
        # All models failed
        # ==========================================

        if last_error:

            error_text = str(
                last_error
            ).lower()

            if (
                "429" in error_text
                or "quota" in error_text
                or "resource_exhausted"
                in error_text
            ):

                return (
                    "⚠️ تم الوصول إلى حد استخدام "
                    "Gemini API.\n\n"
                    "تحقق من حدود الاستخدام الخاصة "
                    "بـ API Key ثم حاول مرة أخرى."
                )

            if (
                "503" in error_text
                or "unavailable"
                in error_text
                or "capacity"
                in error_text
            ):

                return (
                    "⚠️ Gemini مشغول حاليًا "
                    "أو لا توجد سعة متاحة للموديل.\n\n"
                    "حاول مرة أخرى بعد قليل."
                )

            if (
                "404" in error_text
                or "not found"
                in error_text
            ):

                return (
                    "⚠️ لا يوجد موديل متاح "
                    "لهذا API Key."
                )

            return (
                "⚠️ حدث خطأ أثناء الاتصال بـ Gemini:\n\n"
                + str(last_error)
            )

        return (
            "⚠️ لم أتمكن من الحصول على رد من Gemini."
        )

    # ==========================================
    # Reset Chat
    # ==========================================

    def reset_chat(self):

        self.chat_session = self._create_chat(
            self.model
        )

    # ==========================================
    # Error Handler
    # ==========================================

    @staticmethod
    def _handle_error(error):

        error_text = str(
            error
        ).lower()

        if (
            "api key" in error_text
            or "apikey" in error_text
            or "authentication" in error_text
            or "401" in error_text
        ):

            return (
                "❌ يوجد خطأ في Gemini API Key."
            )

        if (
            "quota" in error_text
            or "resource_exhausted"
            in error_text
            or "429" in error_text
        ):

            return (
                "⚠️ تم تجاوز حد استخدام "
                "Gemini API."
            )

        if (
            "permission" in error_text
            or "403" in error_text
        ):

            return (
                "❌ لا توجد صلاحية لاستخدام "
                "Gemini API."
            )

        if (
            "404" in error_text
            or "not found" in error_text
        ):

            return (
                "❌ موديل Gemini غير متاح."
            )

        if "timeout" in error_text:

            return (
                "⏱️ انتهت مهلة الاتصال بـ Gemini."
            )

        if (
            "503" in error_text
            or "unavailable"
            in error_text
        ):

            return (
                "⚠️ Gemini غير متاح حاليًا بسبب "
                "الضغط أو عدم توفر السعة."
            )

        return (
            "❌ حدث خطأ أثناء الاتصال بـ Gemini:\n\n"
            + str(error)
        )