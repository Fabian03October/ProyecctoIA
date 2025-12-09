import pyttsx3

engine = pyttsx3.init()

def hablar(texto):
    print(f"[VOZ]: {texto}")
    engine.say(texto)
    engine.runAndWait()
