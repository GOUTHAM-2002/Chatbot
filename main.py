# main.py

import json
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
from fetch import fetch_product_info


def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "response.mp3"
    tts.save(filename)
    os.system(f"afplay {filename}")
    os.remove(filename)


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None


def chatbot():
    while True:
        query = recognize_speech()
        if query is None:
            continue

        query = query.lower()
        if 'exit' in query or 'quit' in query:
            speak("Goodbye!")
            break

        # Check if the query is asking about a product
        if 'tell me about' in query:
            product_name = query.replace('tell me about', '').strip()
            product_info = fetch_product_info(product_name)
            if product_info:
                response = f"The {product_info['title']} costs {product_info['cost']}. {product_info['description']}"
                speak(response)
            else:
                speak("I'm sorry, I don't have information on that product.")
        else:
            speak("Please ask about a product.")


if __name__ == "__main__":
    chatbot()
