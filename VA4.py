import os
import requests
import speech_recognition as sr
import pyttsx3

# Google API key for Custom Search
google_api_key = "AIzaSyD4nn6NE_OC3nbFqW7cFkjvwe73qKrSj7s"

# Custom Search Engine ID
custom_search_engine_id = "470590945e2e24e60"

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Sorry, I couldn't process your request.")

# Function to speak response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to perform web search
def web_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={custom_search_engine_id}&q={query}"
    response = requests.get(url)
    data = response.json()
    if "items" in data:
        search_results = [(item["title"], item["snippet"]) for item in data["items"]]
        return search_results
    return []

# Main loop for the personal assistant
if __name__ == "__main__":
    speak("Hello! How can I assist you today?")
    while True:
        query = recognize_speech()
        if query:
            search_results = web_search(query)
            if search_results:
                speak("Here are some search results:")
                for title, snippet in search_results:
                    speak(f"Title: {title}")
                    speak("Summary:")
                    speak(snippet)
            else:
                speak("I'm sorry, I couldn't find any relevant information.")
