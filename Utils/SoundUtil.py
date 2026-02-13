import pyttsx3
import threading


def play_sound(word):
    def _speak():
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.say(word)
        engine.runAndWait()
        engine.stop()

    threading.Thread(target=_speak, daemon=True).start()