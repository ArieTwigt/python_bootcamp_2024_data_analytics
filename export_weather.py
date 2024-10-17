import requests
from dotenv import load_dotenv
import pandas as pd
import os


# load the environment variables
load_dotenv()

# get the API key
api_key = os.environ.get('WEATHER_MAP_KEY')

# get the name of the input city
cities = input("Which cities:\n").split(" ")

for city in cities:

    # define the endpoint
    endpoint = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    # execute the request
    response = requests.get(endpoint)

    # get the data from the response
    data = response.json()


    # initiate the lists
    temperatures = []
    feels_like_temperatures = []
    descriptions = []
    dates = []
    wind_speeds = []


    for prediction in data['list']:
        temperatures.append(prediction['main']['temp'])
        feels_like_temperatures.append(prediction['main']['feels_like'])
        descriptions.append(prediction['weather'][0]['description'])
        dates.append(prediction['dt_txt'])   
        wind_speeds.append(prediction['wind']['speed'])

    # compose the data frame
    df_weather = pd.DataFrame({
        'date': dates,
        'temperature': temperatures,
        'temperature_feels_like': feels_like_temperatures,
        'description': descriptions,
        'wind_speed': wind_speeds
    })

    # export to excel
    col_names = ['Datum', 'Temperatuur', 'Gevoelstemperatuur', 'Beschrijving', 'Windsnelheid']

    with pd.ExcelWriter('data/export/weather_predictions.xlsx', 
                        mode='a', 
                        if_sheet_exists='replace') as writer:
        df_weather.to_excel(writer, sheet_name=f"{city}", index=False)
