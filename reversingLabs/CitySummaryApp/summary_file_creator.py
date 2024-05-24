import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CitySummaryApp.city_info_service import CityInfoService

class CitySummaryFileCreator():

    def create_city_summary_file(self, city: str) -> str:
        """
        Crate short summary file about given city with its current temperature.
        """
        summaries_dir = 'city_summaries'
        file_path = os.path.join( os.getcwd(), summaries_dir, f'{city.lower().replace(" ", "_")}.txt')

        # Create the directory city_summaries if it does not exist
        os.makedirs(summaries_dir, exist_ok=True)

        summary = self.__create_city_summary(city)
        with open(file_path, 'w') as file:
            file.write(summary)
        return file_path

    def __create_city_summary(self, city: str) -> str:
        city_info_service: CityInfoService = CityInfoService(city)
        city_temp = city_info_service.get_city_temp()
        city_summary = city_info_service.get_city_summary()
        return city_summary + f" \n \nCurrent temperature in {city} is {city_temp} degrees Celsius."
        
     