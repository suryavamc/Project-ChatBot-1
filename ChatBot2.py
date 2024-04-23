import os
import requests
import json
import subprocess
import webbrowser

# Define the chatbot's response
def respond(query):
    # Set up the Bing search API client
    subscription_key = "0d9dd25639624d298b7dadcdf996bcc3"
    search_url = "https://api.bing.microsoft.com/v7.0/search"

    # Set up the search query
    params = {
        "q": query,
        "count": 10,
        "offset": 0,
        "mkt": "en-US",
        "safeSearch": "Moderate",
    }

    # Send the search query to the Bing search API
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.get(search_url, headers=headers, params=params)

    # Extract the search results from the API response
    search_results = response.json()
    if "webPages" in search_results:
        web_pages = search_results["webPages"]
        if "value" in web_pages:
            return web_pages["value"]
    return []

# Define the chatbot's behavior
def behave(query):
    # Open web pages
    if "open" in query and "google" in query:
        webbrowser.open("https://www.google.com")
        return "Opening Google in your default browser..."

    # Search for images
    if "show me" in query and "images" in query:
        image_query = query.replace("show me", "").replace("images", "")
        search_results = search_bing(image_query)
        if search_results:
            image_urls = [result["contentUrl"] for result in search_results]
            subprocess.Popen(["start", image_urls[0]])
            return "Showing images related to {} in your default browser...".format(image_query)

    # Play music
    if "play" in query and "music" in query:
        music_query = query.replace("play", "").replace("music", "")
        subprocess.Popen(["start", "https://www.youtube.com/results?search_query={}".format(music_query)])
        return "Playing music related to {} in your default browser...".format(music_query)

    # Default behavior
    search_results = respond(query)
    if search_results:
        response_text = ""
        for result in search_results:
            response_text += result["name"] + " (" + result["url"] + ")\n"
        return response_text
    return "I'm sorry, I couldn't find any results for that query."

# Run the chatbot
if __name__ == "__main__":
    while True:
        # Get user input
        query = input("You: ")

        # Handle user input
        response_text = behave(query)

        # Print the chatbot's response
        print("Chatbot: " + response_text)
