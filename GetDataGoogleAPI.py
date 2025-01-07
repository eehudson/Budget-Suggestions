import requests

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

def get_mode():
    ### Asks for a mode of transportation and returns it in a form that can be fed in a search query ###
    mode = input("Are you driving, walking, bicycling, or using transit?: ")
    mode = mode.lower().strip()

    #Error checks to make sure the mode is written in the right format 
    if mode not in ['driving','walking','bicycling','transit']:
        mode = input('Invalid input. Just enter driving, walking, bycycling, or transit:')
        mode.lower().strip()
    else:
        mode = mode
    return mode 

def get_key():
    API_KEY = input("Please enter your API Key. WARNING. DO NOT ENTER API KEY ON PUBLIC FORUM. CASE SENSITIVE.: ")
    return API_KEY

def get_route_data(api_key, origin, destination):
    ### Takes in api_key, origin, and destination and returns route data using Google Maps API ###

    # Base URL for the Google Maps Directions API
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    
    # Parameters for the API request
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,  # Options: driving, walking, bicycling, transit
        "key": api_key
    }
    
    # Make the API request
    response = requests.get(base_url, params=params)
    
    # Check the response status
    if response.status_code == 200:
        data = response.json()
        # print(data) # Uncomment this line to use it as a debugger to see if your I.P. address was denied 
        if data["status"] == "OK":
            # Extract route information
            routes = data["routes"]
            for route in routes:
                print("Summary:", route["summary"])
                print("Legs:")
                for leg in route["legs"]:
                    print(f"  Start Address: {leg['start_address']}")
                    print(f"  End Address: {leg['end_address']}")
                    print(f"  Distance: {leg['distance']['text']}")
                    print(f"  Duration: {leg['duration']['text']}")
                    print(f" Your mode of transportation is : {mode}")
        else:
            print("Error:", data["status"])
    else:
        print("Failed to connect to the API. Status Code:", response.status_code)

# Replace with your actual Google Maps API key
API_KEY = get_key()

# Define the origin and destination
origin = get_origin()
destination = get_destination()
mode = get_mode()

# Get route data
get_route_data(API_KEY, origin, destination)