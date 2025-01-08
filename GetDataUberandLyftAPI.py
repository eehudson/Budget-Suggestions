import requests

#DEFINE FUNCTIONS 

def get_origin():
    ### Asks for an origin address or location and returns it in a form that can be passed in a search query ###
    origin = input("Please enter the starting location as an address or city: ") 
    origin = origin.replace(',','') #rewrites in google's api format 
    origin = origin.replace(' ','+') #rewrites in google's api format 
    return origin


def get_destination():
    ### Asks for a desination address or location and returns it in a form that can be passed in a search query ###
    destination = input("Please enter the ending location as an address or city: ") 
    destination = destination.replace(' ','+') #rewrites in google's api format 
    return destination

def get_lat_lng(google_api_key, address):
    ### Asks user for API key and an address and converts it to a latitude and longitude coordinate ###
    #Base URL for the Geocoding API 
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    # Parameters for the API request
    params = {
        "address": address,
        "key": google_api_key,
    }
    
    # Make the API request
    response = requests.get(base_url, params=params)
    
    # Check the response status
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            # Extract latitude and longitude
            location = data["results"][0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            print(f"Address: {address}")
            print(f"Latitude: {latitude}, Longitude: {longitude}")
            return latitude, longitude
        else:
            print("Error:", data["status"], "-", data.get("error_message", "Unknown error"))
    else:
        print("Failed to connect to the API. Status Code:", response.status_code)

def get_uber_access_token(client_id, client_secret):
    ### Gets an uber access token that you can use as an API key ###
    oauth_url = "https://login.uber.com/oauth/v2/token"

    # Replace these with your actual client ID and client secret
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"

    # Request body
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "rides.request"  # Modify as needed
    }
    # Make the request
    response = requests.post(oauth_url, data=data)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("Access Token:", access_token)
        return access_token
    else:
        print("Failed to obtain access token:", response.json())

def get_key():
    ### Asks the user for the API Key and returns it ###
    API_KEY = input("Please enter your API Key. WARNING. DO NOT ENTER API KEY ON PUBLIC FORUM. CASE SENSITIVE.: ")
    return API_KEY

def get_client_id():
    client_id = input("Please enter your UBER Client Id: ")
    return client_id

def get_client_secret():
    client_secret = input("Please enter your UBER Client Secret: ")
    return client_secret

def get_uber_estimates(uber_api_key, start_lat, start_lng, end_lat, end_lng):
    ### Returns Uber Price Estimates based off of starting latitude and longitude ###
    url = "https://api.uber.com/v1.2/estimates/price"
    headers = {
        "Authorization": f"Token {uber_api_key}",
        "Content-Type": "application/json",
    }
    params = {
        "start_latitude": start_lat,
        "start_longitude": start_lng,
        "end_latitude": end_lat,
        "end_longitude": end_lng,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        print("Uber Estimates:")
        for ride in data.get("prices", []):
            print(f"{ride['display_name']}: {ride['estimate']}, Duration: {ride['duration']/60:.1f} mins, Distance: {ride['distance']} miles")
    else:
        print("Error fetching Uber data:", response.json())


def get_lyft_estimates(lyft_api_key, start_lat, start_lng, end_lat, end_lng):
    ### Gives lyft price estimates based off of starting latitude and longitude ###
    # Lyft API URL for cost estimates
    url = "https://api.lyft.com/v1/cost"
    headers = {
        "Authorization": f"Bearer {lyft_api_key}",
    }
    params = {
        "start_lat": start_lat,
        "start_lng": start_lng,
        "end_lat": end_lat,
        "end_lng": end_lng,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        print("Lyft Estimates:")
        for ride in data.get("cost_estimates", []):
            min_cost = ride["estimated_cost_cents_min"] / 100
            max_cost = ride["estimated_cost_cents_max"] / 100
            print(f"{ride['ride_type'].capitalize()}: ${min_cost}-{max_cost}, Duration: {ride['estimated_duration_seconds']/60:.1f} mins, Distance: {ride['estimated_distance_miles']} miles")
    else:
        print("Error fetching Lyft data:", response.json())

## RUN FUNCTIONS

# Get API Keys 
print("Please enter your Google API key: ")
GOOGLE_API_KEY = get_key()

print("Please enter your Lyft API key: ")
LYFT_API_KEY = get_key()

print("Please enter your UBER Information: ")
client_id = get_client_id()
client_secret = get_client_secret()
UBER_API_KEY = get_uber_access_token(client_id, client_secret)

# Coordinates for origin and destination
origin = get_origin()
destination = get_destination()
start_latitude, start_longitude = get_lat_lng(GOOGLE_API_KEY,origin) 
end_latitude, end_longitude = get_lat_lng(GOOGLE_API_KEY,destination)


# Get Price Estimates 
print("Fetching Uber Estimates...")
get_uber_estimates(UBER_API_KEY, start_latitude, start_longitude, end_latitude, end_longitude)

print("\nFetching Lyft Estimates...")
get_lyft_estimates(LYFT_API_KEY, start_latitude, start_longitude, end_latitude, end_longitude)
