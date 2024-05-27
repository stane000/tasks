import argparse
from summary_file_creator import CitySummaryFileCreator

def main():
    
    parser = argparse.ArgumentParser(description="City Summary Generator")
    parser.add_argument('city', type=str, help='Name of the city to get the summary for')
    try:
    
        args = parser.parse_args()
        city_name = args.city

        if city_name == "":
            raise Exception("Entered value can't be empty string") 

        path = CitySummaryFileCreator().create_city_summary_file(city_name)
    except Exception as ex:
        print(f"{ex}")
    else:
        print(f"Summary created, path: {path}")
    
if __name__ == "__main__":
    main()
