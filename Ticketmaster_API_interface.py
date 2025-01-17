# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 10:46:45 2025

@author: utley
"""

import requests

API_KEY = input("Provide API key: ")    #DO NOT INCLUDE ON GITHUB
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def search_events(keyword=None, location=None, radius=None, start_date=None, end_date=None):
    """
    Search for events using the Ticketmaster Discovery API.
    
    :param keyword: Search term for events (e.g., "concert", "sports")
    :param location: Tuple of latitude and longitude (e.g., (34.0522, -118.2437) for Los Angeles)
    :param radius: Search radius in miles (e.g., 50 for 50 miles)
    :param start_date: Start date in ISO 8601 format (e.g., "2025-01-01T00:00:00Z")
    :param end_date: End date in ISO 8601 format (e.g., "2025-01-31T23:59:59Z")
    :return: List of events or error message
    """
    params = {
        "apikey": API_KEY,
        "keyword": keyword,
        "radius": radius,
        "startDateTime": start_date,
        "endDateTime": end_date,
        "locale": "*",  # Accept all locales
        "size": 20,  # Number of results per page
    }
    
    # Add geolocation parameters if provided
    if location:
        params["latlong"] = f"{location[0]},{location[1]}"
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "_embedded" in data and "events" in data["_embedded"]:
            events = data["_embedded"]["events"]
            return [
                {
                    "name": event["name"],
                    "date": event["dates"]["start"]["localDate"],
                    "time": event["dates"]["start"].get("localTime", "TBA"),
                    "venue": event["_embedded"]["venues"][0]["name"],
                    "url": event["url"],
                }
                for event in events
            ]
        else:
            return "No events found."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Example usage
if __name__ == "__main__":
    keyword = input("What do you want to go see? ")
    location = (42.2056, -71.0601)  # Boston University
    radius = 35
    start_date = "2025-01-01T00:00:00Z"      #Need to include UI start and end date selection
    end_date = "2025-01-31T23:59:59Z"
    
    events = search_events(keyword=keyword, location=location, radius=radius, start_date=start_date, end_date=end_date)
    if isinstance(events, list):
        for event in events:
            print(f"Event: {event['name']}")
            print(f"Date: {event['date']} Time: {event['time']}")
            print(f"Venue: {event['venue']}")
            print(f"URL: {event['url']}\n")
    else:
        print(events)