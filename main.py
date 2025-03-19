import openai
import json
import requests
from flask import Flask, request, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

# OpenAI API Key (yahan apni API key daalna)
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

# Hadith Database Load
with open("data/hadiths.json", "r", encoding="utf-8") as f:
    hadith_data = json.load(f)

# AI Response Function
def get_ai_response(user_input):
    prompt = f"Saru Bot: {user_input}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Hadith Fetching Function
def get_hadith(topic):
    for hadith in hadith_data:
        if topic.lower() in hadith["topic"].lower():
            return f"{hadith['text']} - {hadith['source']}"
    return "Mujhe is topic par koi sahih hadith nahi mili."

# Fairness Analysis (Kon sahi, kon galat)
def fairness_analysis(user_msg, ruby_msg):
    if "galti" in user_msg.lower():
        return "Saru: Tumhari baat sahi ho sakti hai, lekin Ruby ki feelings bhi samajhna zaroori hai."
    elif "sorry" in ruby_msg.lower():
        return "Saru: Ruby ne maafi maang li, ab tumhe bhi maamla suljhana chahiye."
    return "Saru: Dono ki baat samajh ke ek behtar faisla lo."

# Text-to-Speech (TTS) for Voice Messages
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")  # Linux users ke liye, Windows me "start response.mp3"

# Flask API for WhatsApp Integration
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "")
    
    # Agar user "/Nikah" likhe to process start kare
    if user_input.lower() == "/nikah":
        return jsonify({"response": "Kya tum dono Nikah ke liye tayar ho? Reply: 'Yes' ya 'No'"})
    
    # AI Response Generate karo
    response = get_ai_response(user_input)

    # Agar user voice message maange
    if "voice" in user_input.lower():
        text_to_speech(response)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
