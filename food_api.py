
import requests

# Replace this with your Yelp API key
API_KEY = "XJB-mNIW73S4hFLWWKunMcDGnVG60CZxpbe3kLZUXqYnePH1ThBW5VaBne4NLCj7mw6JcrC3mnRIFMIoVhA1WUQpwdQESh6xfx4ON8n4U-yNlKS_Tvbl-FacYol9Z3Yx"

# Base URL for Yelp API
YELP_API_URL = "https://api.yelp.com/v3/businesses/search"

def get_boston_restaurants(budget_min, budget_max, radius):
    # Map budget range to Yelp price levels
    if budget_max <= 10:
        price = "1"  # $
    elif 10 < budget_max <= 30:
        price = "2"  # $$
    elif 30 < budget_max <= 60:
        price = "3"  # $$$
    else:
        price = "4"  # $$$$

    # API parameters
    params = {
        "location": "Boston, MA",  # Fixed location: Boston
        "categories": "restaurants",
        "price": price,
        "radius": radius,  # Radius in meters
        "limit": 5,  # Get up to 5 suggestions
    }

    # API headers with authorization
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    # Send request to Yelp API
    response = requests.get(YELP_API_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        businesses = data.get("businesses", [])
        if businesses:
            print(f"\nHere are some restaurant suggestions in Boston for ${budget_min}-${budget_max}:")
            for i, business in enumerate(businesses, start=1):
                name = business["name"]
                rating = business["rating"]
                address = ", ".join(business["location"]["display_address"])
                print(f"{i}. {name} - Rating: {rating}/5, Address: {address}")
        else:
            print("No restaurants found for your preferences.")
    else:
        print(f"Error: Unable to fetch data ({response.status_code}).")

# User input for budget range
try:
    budget_min = float(input("Enter your minimum budget ($): "))
    budget_max = float(input("Enter your maximum budget ($): "))

    if budget_min > budget_max:
        print("Invalid input: Minimum budget cannot be greater than maximum budget.")
    else:
        # Define radius in meters (e.g., 5,000 meters = 3 miles)
        radius = 5000

        # Get Boston restaurant suggestions
        get_boston_restaurants(budget_min, budget_max, radius)
except ValueError:
    print("Please enter valid numbers for the budget range.")
