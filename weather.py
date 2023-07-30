import urllib.request as request
import json
import math

RADIUS_OF_EARTH = 6378.1 # km

def points(latitude, longitude):
    # gets the gridpoint associated with a specific point
    # does not accept more than 4 decimal places
    url = f'https://api.weather.gov/points/{latitude:.4f},{longitude:.4f}'
    with request.urlopen(url) as response:
        if response.status != 200:
            raise FileNotFoundError("Could not contact the weather server properly.")
        return response.read()

def forecast(office, gridX, gridY):
    # gets the forecast associated with a gridpoint
    url = f'https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast'
    with request.urlopen(url) as response:
        if response.status != 200:
            raise FileNotFoundError("Could not contact the weather server properly.")
        return response.read()
    
def get_gridpoint_from_loc(latitude, longitude):
    response = json.loads(points(latitude, longitude))

    properties = response['properties']
    return properties['gridId'], properties['gridX'], properties['gridY']


class Region:
    """Assumes a region in the northern hemisphere"""
    def __init__(self, min_latitude, min_longitude, max_latitude, max_longitude, name):
        self.min_latitude = min_latitude
        self.min_longitude = min_longitude
        self.max_latitude = max_latitude
        self.max_longitude = max_longitude
        self.name = name

        # each cell is 2.5km by 2.5km
        # the longitude degrees per cell depends on the latitude, so we pick 
        # the smallest spacing to ensure we get all cells
        degrees_latitude_per_cell = 2.5 / RADIUS_OF_EARTH * 360 / (2 * math.pi)
        degrees_longidue_per_cell = 2.5 / RADIUS_OF_EARTH * 360 / (2 * math.pi) * math.cos(min(self.min_latitude, self.max_latitude))

# use 
# use /gridpoints/{wfo}/{x},{y}/stations to get the stations
# use /stations/{stationId}/observations to get the observations from the stations
# or maybe /stations/{stationId}/observations/latest