import os
import requests
import json

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

# Run the chatbot
if __name__ == "__main__":
    while True:
        # Get user input
        query = input("You: ")

        # Handle user input
        response_text = ""
        search_results = respond(query)
        if search_results:
            for result in search_results:
                response_text += result["name"] + " (" + result["url"] + ")\n"

        # Print the chatbot's response
        print("Chatbot: " + response_text)
