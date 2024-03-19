''' file for support functions for the main.py file '''


from geopy.geocoders import Nominatim, Photon, OpenCage, Geokeo
import os
from dotenv import load_dotenv

load_dotenv()


OPENCAGE_KEY = os.getenv("OPENCAGE")
GEOKEO_KEY = os.getenv("GEOKEO")


api_keys = {
    "<class 'geopy.geocoders.opencage.OpenCage'>": OPENCAGE_KEY,
    "<class 'geopy.geocoders.geokeo.Geokeo'>": GEOKEO_KEY
}

with_api_key = [OpenCage, Geokeo]
without_api_key = [Nominatim, Photon]


def get_name_by_coordinates(lat: float | int, lon: float | int):
    """    Get the name of a location based on its coordinates.

    This function takes latitude and longitude coordinates as input and uses geocoders to retrieve the location name.
    It first tries to retrieve the location name using geocoders without API keys, and if unsuccessful, it tries with API keys.

    Args:
        lat (float | int): The latitude coordinate of the location.
        lon (float | int): The longitude coordinate of the location.

    Returns:
        str: The name of the location based on the input coordinates.

    Raises:
        Exception: If there is an error while retrieving the location name.
    """


    for geocoder in without_api_key:
        geolocator = geocoder(user_agent="geoapiExercises")
        try:
            location = geolocator.reverse([lat, lon])
            return location.address
        except Exception as e:
            print(e)
            continue
    for geocoder in with_api_key:
        print(geocoder)
        geolocator = geocoder((api_keys[str(geocoder)]))
        location = geolocator.reverse([lat, lon])
        try:
            if location.address:

                return location.address
        except Exception as e:
            print(e)
            continue
    return None


if __name__ == '__main__':
    print(get_name_by_coordinates(25.439121, 84.872330))
