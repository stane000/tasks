from typing import Optional
import requests
from requests import Response
from requests.exceptions import ConnectionError, Timeout, RequestException, HTTPError

API_KEY = '7eb62fe6f1de3ed719817a06df6963e1'

class CityInfoService():

    """

    This class provides methods to retrieve temperature and summary information for a given city.

    Attributes:
        city (str): The name of the city.

    Methods:
        __init__: Initializes the CityInfoService with the specified city.
        get_city_temp: Retrieves the temperature of the city from OpenWeatherMap API.
        get_city_summary: Retrieves the summary of the city from Wikipedia API.
    """

    __slots__ = "city"
    city: str

    def __init__(self, city: str) -> None:
        self.city = city
     
    def get_city_temp(self) -> str:
        """
        Retrieves the temperature of the city from OpenWeatherMap API.
        """
        response = self.__send_get_request(f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={API_KEY}&units=metric")
        return response.json()['main']['temp'] 
    
    def get_city_summary(self) -> str:
        """
        Retrieves the summary of the city from Wikipedia API.
        """
        response = self.__send_get_request("https://en.wikipedia.org/api/rest_v1/page/summary/" + self.city)
        return response.json()['extract']
    
    def __send_get_request(self, url) -> Optional[Response]:
        """
        Created only for better requests error readability
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        
        except HTTPError as http_err:

            if response.status_code == 401:
                raise HTTPError("Error: Unauthorized. The API key is invalid or expired.")
            elif response.status_code == 403:
                raise HTTPError("Error: Forbidden. The API key does not have the necessary permissions.")
            elif response.status_code == 404:
                raise HTTPError(f"City {self.city} not exists in database")
            else:
                raise HTTPError(f"HTTP error occurred: {http_err}")  

        except ConnectionError:
                raise ConnectionError("Error: Connection error. Please check your network connection.")
        except Timeout:
                raise Timeout("Error: Timeout. The request took too long to complete.")
        except RequestException as err:
                raise RequestException(f"Error: An error occurred. {err}")  

