import os
import requests
import json
import subprocess
import webbrowser
import speech_recognition as sr
from gtts import gTTS
import playsound

# Define the Google search API key and Custom Search Engine ID
google_api_key = "AIzaSyD4nn6NE_OC3nbFqW7cFkjvwe73qKrSj7s"
google_cse_id = "470590945e2e24e60"

# Define the Bing search API subscription key
bing_subscription_key = "0d9dd25639624d298b7dadcdf996bcc3"

# Define the chatbot's response using Google Custom Search JSON API
def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={google_cse_id}&q={query}"
    response = requests.get(url)
    data = response.json()
    if "items" in data:
        return [item["link"] for item in data["items"]]
    return []

# Define the chatbot's response using Bing Search API
def bing_search(query):
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_subscription_key}
    params = {"q": query, "count": 10, "mkt": "en-US"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if "webPages" in data:
        web_pages = data["webPages"]
        if "value" in web_pages:
            return [item["url"] for item in web_pages["value"]]
    return []

# Define the chatbot's behavior
def behave(query):
    # Voice recognition
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            print("You said: " + query)
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            print("Sorry, I couldn't process your request.")
            return "Sorry, I couldn't process your request."

    # Process the query using Google Search API
    google_results = google_search(query)
    if google_results:
        response_text = "Google Search Results:\n"
        for result in google_results:
            response_text += result + "\n"
    else:
        # Process the query using Bing Search API
        bing_results = bing_search(query)
        if bing_results:
            response_text = "Bing Search Results:\n"
            for result in bing_results:
                response_text += result + "\n"
        else:
            response_text = "I'm sorry, I couldn't find any results for that query."

    return response_text

# Run the virtual assistant
if __name__ == "__main__":
    while True:
        response_text = behave("")

        # Print the virtual assistant's response
        print("Virtual Assistant: " + response_text)
