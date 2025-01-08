#MAIN FILE 

#IMPORT LIBRARIES 
import requests
from datetime import datetime
from googlefunctions import google_is_open_at_time
from googlefunctions import get_google_places
from googlefunctions import get_google_key

#HARD CODE LOCATION AND DISTANCE 
location = "42.3601,-71.0589" #Coordinates for Boston, MA
radius = 40 #40,000m 

#STEP ONE: Get information parsed into dictionary
parameters = {"budget": 1,
              "type": "Concert",
              "date": "MM/DD/YYYY",
              "time": ""}


#SEARCH BASED ON SUGGESTION
if parameters["type"] == "restaurants" or "active" or "nightlife":
    #ADD YELP
    #GET YELP_API_KEY

    #SEARCH RESULTS

    #FORMAT SEARCH RESULTS

elif parameters["type"] == "events":
    #ADD TICKETMASTER CODE 


elif parameters["type"] == "natural_feature" or "museum" or "park":
    #ADD GOOGLE CODE 
    google_api_key = get_google_key() #Get the users google api key
    place_type = parameters["type"]
    target_datetime = datetime(parameters["date"])
    places = get_google_places(google_api_key, location, radius, minprice, maxprice, place_type, target_datetime) #get places and store them in a list 

    #NEXT FIGURE OUT HOW TO DISPLAY 

else:
    print("Wrong parameter. Start again.")


#TO DO: Come back to google and figure out how to code min price and max price categories 
