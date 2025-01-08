import requests

def get_key():
    ### Asks the user for the API Key and returns it ###
    API_KEY = input("Please enter your API Key. WARNING. DO NOT ENTER API KEY ON PUBLIC FORUM. CASE SENSITIVE.: ")
    return API_KEY


# Replace with your Eventbrite API key


# Base URL for Eventbrite API
BASE_URL = "https://www.eventbriteapi.com/v3/events/search/"

# Function to search for events based on cost and distance
def search_events(eventbrite_key, location, radius, price, category=None):
    """
    Search for events on Eventbrite based on cost and distance.
    
    :param location: The latitude and longitude as a string, e.g., "37.7749,-122.4194".
    :param radius: The search radius in kilometers, e.g., "10km".
    :param price: The price filter, e.g., "free" or "paid".
    :param category: (Optional) The category ID for events, e.g., "103" for music.
    :return: A list of events matching the criteria.
    """
    headers = {"Authorization": f"Bearer{eventbrite_key}"}
    params = {
        "location.latitude": location.split(",")[0],
        "location.longitude": location.split(",")[1],
        "location.within": radius,
        "price": price,
        "sort_by": "distance",  # Sort results by proximity
    }
    if category:
        params["categories"] = category
    
    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()["events"]
    else:
        print("Error:", response.status_code, response.json())
        return []

# Example usage
    # Replace with your location (latitude, longitude), radius, and price filter


eventbrite_key = get_key()

location = "Boston, MA"  # San Francisco, CA
radius = "10km"
price = "free"  # Use "paid" for paid events
category = None  # Optional: add a category ID
    
events = search_events(eventbrite_key, location, radius, price, category)

if events:
    print(f"Found {len(events)} events:")
    for event in events:
        print(f"- {event['name']['text']} (URL: {event['url']})")
else:
    print("No events found.")
