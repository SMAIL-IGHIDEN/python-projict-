import openai
import pyttsx3
import sounddevice as sd
import numpy as np
import wavio

# 🔑 ضع هنا API KEY ديالك
openai.api_key = "YOUR_OPENAI_API_KEY"

# إعداد الصوت
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # سرعة الكلام
engine.setProperty('volume', 1.0)

# تسجيل الصوت
def record_audio(duration=5, fs=44100):
    print("سجّل كلامك دابا...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write("input.wav", recording, fs, sampwidth=2)
    print("تم التسجيل ✅")
    return "input.wav"

# تحويل الصوت إلى نص (STT) باستعمال Whisper
def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text

# إرسال النص ل OpenAI ChatGPT والرد
def ask_openai(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

# التحدث بالصوت
def speak(text):
    engine.say(text)
    engine.runAndWait()

# 🔁 الحلقة الرئيسية
if __name__ == "__main__":
    while True:
        audio_file = record_audio(duration=5)  # سجل 5 ثواني
        text = transcribe_audio(audio_file)
        print("انت قلت:", text)
        reply = ask_openai(text + " بالدارجة المغربية")
        print("روبوت:", reply)
        speak(reply)
