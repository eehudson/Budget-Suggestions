import requests

def get_lat_lng(api_key, address):
    # Base URL for the Geocoding API
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    # Parameters for the API request
    params = {
        "address": address,
        "key": api_key
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

# Replace with your actual Google Maps API key
API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

# Example address
address = "Boston, MA"

# Get latitude and longitude
get_lat_lng(API_KEY, address)

def get_uber_estimates(api_key, start_lat, start_lng, end_lat, end_lng):
    ### Returns Uber Price Estimates for a Ride Uber API URL for price estimates
    url = "https://api.uber.com/v1.2/estimates/price"
    headers = {
        "Authorization": f"Token {api_key}",
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

def get_lyft_estimates(api_key, start_lat, start_lng, end_lat, end_lng):
    # Lyft API URL for cost estimates
    url = "https://api.lyft.com/v1/cost"
    headers = {
        "Authorization": f"Bearer {api_key}",
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

# Replace these with your API keys
UBER_API_KEY = "YOUR_UBER_API_KEY"
LYFT_API_KEY = "YOUR_LYFT_API_KEY"

# Coordinates for origin and destination
start_latitude = 42.3601  # Boston Latitude
start_longitude = -71.0589  # Boston Longitude
end_latitude = 42.3736  # Cambridge Latitude
end_longitude = -71.1097  # Cambridge Longitude

# Fetch estimates
print("Fetching Uber Estimates...")
get_uber_estimates(UBER_API_KEY, start_latitude, start_longitude, end_latitude, end_longitude)

print("\nFetching Lyft Estimates...")
get_lyft_estimates(LYFT_API_KEY, start_latitude, start_longitude, end_latitude, end_longitude)
