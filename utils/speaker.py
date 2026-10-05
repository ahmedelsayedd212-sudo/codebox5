import asyncio
import os
import re
import tempfile
import threading

import edge_tts

# pygame is optional
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    pygame = None
    PYGAME_AVAILABLE = False


class Speaker:
    """Professional Text-To-Speech system for CodeBox."""

    def __init__(self):
        self.arabic_voice = "ar-EG-SalmaNeural"
        self.english_voice = "en-US-JennyNeural"

        self.stop_requested = False
        self.is_speaking = False
        self.thread = None

        # Initialize pygame only if available
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
            except Exception:
                self._pygame_ready = False
            else:
                self._pygame_ready = True
        else:
            self._pygame_ready = False

    # ==========================================
    # Clean Text
    # ==========================================

    def clean_text(self, text: str) -> str:

        if not text:
            return ""

        text = re.sub(
            r"```.*?```",
            "",
            text,
            flags=re.DOTALL,
        )

        text = text.replace("**", "")
        text = text.replace("__", "")
        text = text.replace("*", "")
        text = text.replace("_", " ")

        text = re.sub(
            r"^#+\s*",
            "",
            text,
            flags=re.MULTILINE,
        )

        text = re.sub(
            r"\[([^\]]+)\]\([^)]+\)",
            r"\1",
            text,
        )

        text = text.replace("`", "")

        text = re.sub(
            r"^\s*[-•]\s*",
            "",
            text,
            flags=re.MULTILINE,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # ==========================================
    # Detect Language
    # ==========================================

    def is_arabic(self, text: str) -> bool:

        arabic_count = 0
        english_count = 0

        for char in text:

            if "\u0600" <= char <= "\u06ff":
                arabic_count += 1

            elif char.isalpha():
                english_count += 1

        return arabic_count > english_count

    # ==========================================
    # Generate Audio
    # ==========================================

    async def _generate_audio(
        self,
        text,
        voice,
        filename,
    ):

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate="+0%",
            volume="+0%",
        )

        await communicate.save(filename)

    # ==========================================
    # Speak
    # ==========================================

    def speak(self, text: str):

        text = self.clean_text(text)

        if not text:
            return

        # Streamlit Cloud / server
        # does not have local audio playback.
        if not self._pygame_ready:
            print("Audio playback is unavailable in this environment.")
            return

        self.stop()

        self.stop_requested = False

        self.thread = threading.Thread(
            target=self._speak_worker,
            args=(text,),
            daemon=True,
        )

        self.thread.start()

    # ==========================================
    # Worker
    # ==========================================

    def _speak_worker(self, text):

        temp_file = None

        try:

            self.is_speaking = True

            if self.is_arabic(text):
                voice = self.arabic_voice
            else:
                voice = self.english_voice

            with tempfile.NamedTemporaryFile(
                suffix=".mp3",
                delete=False,
            ) as file:

                temp_file = file.name

            asyncio.run(
                self._generate_audio(
                    text,
                    voice,
                    temp_file,
                )
            )

            if self.stop_requested:
                return

            pygame.mixer.music.load(temp_file)

            if self.stop_requested:
                return

            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():

                if self.stop_requested:

                    pygame.mixer.music.stop()

                    break

                pygame.time.Clock().tick(30)

        except Exception as error:

            print(f"Speech Error: {error}")

        finally:

            self.is_speaking = False

            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
            except Exception:
                pass

            if temp_file and os.path.exists(temp_file):

                try:
                    os.remove(temp_file)

                except Exception:
                    pass

    # ==========================================
    # Stop Immediately
    # ==========================================

    def stop(self):

        self.stop_requested = True

        if not self._pygame_ready:
            self.is_speaking = False
            return

        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

        except Exception:
            pass

        self.is_speaking = False

    # ==========================================
    # Status
    # ==========================================

    def is_playing(self):

        if not self._pygame_ready:
            return False

        try:
            return pygame.mixer.music.get_busy()

        except Exception:
            return False

    # ==========================================
    # Cleanup
    # ==========================================

    def cleanup(self):

        self.stop()

        if not self._pygame_ready:
            return

        try:
            pygame.mixer.quit()

        except Exception:
            pass
