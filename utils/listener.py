import speech_recognition as sr


class Listener:
    """
    CodeBox Voice Listener

    يستمع لصوت المستخدم من الميكروفون
    ويحوّله إلى نص.
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()

        # تقليل حساسية الضوضاء
        self.recognizer.energy_threshold = 300

        # ضبط مدة انتظار الكلام
        self.recognizer.pause_threshold = 0.8

        # أقصى مدة انتظار لبدء الكلام
        self.recognizer.phrase_threshold = 0.3

    def listen(self, language="ar-EG"):
        """
        الاستماع من الميكروفون وتحويل الصوت إلى نص.

        language:
            ar-EG = عربي
            en-US = English
        """

        try:

            with sr.Microphone() as source:

                print("🎤 Listening...")

                # ضبط الميكروفون حسب صوت المكان
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                print("🗣️ Speak now...")

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=15
                )

            print("🧠 Processing...")

            text = self.recognizer.recognize_google(
                audio,
                language=language
            )

            return text

        except sr.WaitTimeoutError:

            return "⏱️ لم أسمع أي كلام."

        except sr.UnknownValueError:

            return "❓ لم أستطع فهم الكلام."

        except sr.RequestError as error:

            return f"❌ حدث خطأ في خدمة التعرف على الصوت: {error}"

        except Exception as error:

            return f"❌ حدث خطأ في الميكروفون: {error}"

    def listen_arabic(self):
        """الاستماع باللغة العربية."""

        return self.listen(
            language="ar-EG"
        )

    def listen_english(self):
        """الاستماع باللغة الإنجليزية."""

        return self.listen(
            language="en-US"
        )
