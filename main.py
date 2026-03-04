'''
You will run this problem set from main.py so set things up accordingly
'''
from src.extract import extract_weather_data, extract_transit_data
from src.transform_load import merge_and_transform

# Call functions / instanciate objects from the two analysis .py files
def main():
        # Call functions from extract.py
        extract_weather_data()
        extract_transit_data()

        # Call functions from transform_load.py
        merge_and_transform()


if __name__ == "__main__":
        main()