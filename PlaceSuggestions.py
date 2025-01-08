import requests
from datetime import datetime

def get_places(api_key, location, radius, minprice, maxprice, place_type, target_datetime):
    # Step 1: Get nearby places
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "key": api_key,
        "location": location,  # Example: "42.3601,-71.0589" for Boston
        "radius": radius,      # Example: 5000 (5km)
        "type": place_type,    # Example: "tourist_attraction", "museum"
        "minprice": minprice,  # Price filter: 0 = Free, 4 = Very expensive
        "maxprice": maxprice,
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return []

    places_data = response.json().get("results", [])
    
    # Step 2: Check business hours with Places Details API
    detailed_results = []
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    for place in places_data:
        place_id = place["place_id"]
        details_params = {
            "key": api_key,
            "place_id": place_id,
            "fields": "name,vicinity,opening_hours,price_level,rating"
        }
        
        details_response = requests.get(details_url, params=details_params)
        if details_response.status_code != 200:
            continue
        
        details_data = details_response.json().get("result", {})
        opening_hours = details_data.get("opening_hours", {})
        
        # Step 3: Filter by target time and date
        if opening_hours.get("open_now"):
            periods = opening_hours.get("periods", [])
            if is_open_at_time(periods, target_datetime):
                detailed_results.append({
                    "name": details_data["name"],
                    "address": details_data.get("vicinity"),
                    "rating": details_data.get("rating"),
                    "price_level": details_data.get("price_level"),
                    "open_now": opening_hours.get("open_now")
                })
    
    return detailed_results

def is_open_at_time(periods, target_datetime):
    target_day = target_datetime.weekday()  # 0 = Monday, 6 = Sunday
    target_time = int(target_datetime.strftime("%H%M"))  # Convert to HHMM format
    
    for period in periods:
        if period["open"]["day"] == target_day:
            open_time = int(period["open"]["time"])
            close_time = int(period["close"]["time"])
            
            # Handle cases where close_time is past midnight
            if close_time < open_time:
                close_time += 2400
            
            if open_time <= target_time <= close_time:
                return True
    return False

# Example usage
api_key = 
location = "42.3601,-71.0589"  # Boston, MA
radius = 5000  # 5km
minprice = 0  # Free
maxprice = 2  # Moderately priced
place_type = "tourist_attraction"
target_datetime = datetime(2025, 1, 8, 15, 0)  # January 8, 2025, 3:00 PM

places = get_places(api_key, location, radius, minprice, maxprice, place_type, target_datetime)
for place in places:
    print(place)
