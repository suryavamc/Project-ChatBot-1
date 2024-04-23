import os
import webbrowser
import requests
import speech_recognition as sr
import subprocess
from gtts import gTTS
import playsound

# Define the Google search API key and Custom Search Engine ID
google_api_key = "AIzaSyD4nn6NE_OC3nbFqW7cFkjvwe73qKrSj7s"
google_cse_id = "470590945e2e24e60"


# Define the chatbot's response using Google Custom Search JSON API
def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={google_cse_id}&q={query}"
    response = requests.get(url)
    data = response.json()
    if "items" in data:
        return [item["link"] for item in data["items"]]
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
    search_results = google_search(query)
    if search_results:
        response_text = "Google Search Results:\n"
        for result in search_results:
            response_text += result + "\n"

            # Open the search result in a web browser
            webbrowser.open(result)

    else:
        # Open applications or browse the web based on the query
        if "open" in query:
            app_name = query.replace("open", "").strip()
            if os.path.exists(app_name):
                subprocess.Popen(app_name)
            else:
                print(f"Could not find application '{app_name}'.")
        elif "browse" in query:
            url = query.replace("browse", "").strip()
            if "http" in url:
                webbrowser.open(url)
            else:
                print(f"Invalid URL '{url}'.")
        else:
            # Default behavior: perform a search query
            response_text = "Search Results:\n"
            for result in search_results:
                response_text += result + "\n"

    return response_text

# Run the virtual assistant
if __name__ == "__main__":
    while True:
        response_text = behave("")

        # Print the virtual assistant's response
        print("Virtual Assistant: " + response_text)

        # Convert the response text to speech
        tts = gTTS(response_text, lang="en")
        tts.save("response.mp3")
        playsound.playsound("response.mp3")

        # Remove the response audio file
        os.remove("response.mp3")
