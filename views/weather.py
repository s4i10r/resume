import streamlit as st 
import requests
import matplotlib.pyplot as plt
import datetime
import pandas as pd


# openweathermap
API_KEY=st.secrets["openweathermap"]["api_key"]
GEO_URL="https://api.openweathermap.org/geo/1.0/direct"

# meteo
BASE_URL="https://api.open-meteo.com/v1/forecast"

# FUNCTIONS

def fetch_geodata(params:dict):
    """
    fetch geodata of city from openweathermap

    Args:
        params (dict):  parameters including the cities name

    Returns:
        dict: dictionary of geodata (longitude, latitude, ...)
    """
    try:
        response = requests.get(GEO_URL, params=params)
        geodata = response.json()

        if response.status_code == 200:
            return geodata
        else:
            st.error(f"Couldnt find data for {params["q"]}.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching geodata: {e}")
        return None




def fetch_weather_data(geodata:dict):
    """
    fetches the weather of a given location (7 days)

    Args:
        geodata (dict)  : longitude and latitude of a given location

    Returns:
        dict: returns weather forecast data (7 days) including today as a json file 
    """
    if not geodata:
        return None

    # required parameters for the meteo api call
    params = {
        "latitude": geodata[0]["lat"],
        "longitude": geodata[0]["lon"],
        "hourly": "temperature_2m",
        "past_days": 2,
    }

    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Couldnt fetch data.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None
    

def process_weather_data(weather_data:dict):
    """
    processes the json file containing the weather forecast to
    a

    Args:
        geodata (dict)  : longitude and latitude of a given location

    Returns:
        dict: returns weather forecast data (7 days) including today as a pandas Dataframe
    """
    if not weather_data:
        return None

    # extract date and temperature
    data = {
        "Date": weather_data["hourly"]["time"],
        "Temperature": weather_data["hourly"]["temperature_2m"]
    }
    df = pd.DataFrame(data)
    # convert date to datetime object
    df["Date"] = pd.to_datetime(df["Date"])

    return df



# Page Layout
st.title("Weather History")

city = st.text_input("Please enter your city", "Frankfurt")


# make diagram
if st.button("Get history"):
    if not city.strip():
        st.error("Please enter a city.")
    else:
        params = {
            "q": city,
            "limit": 1,
            "appid": API_KEY,
        }
        
        # longitude, latitude needed for meteo api call
        city_geodata: dict = fetch_geodata(params)

        # if ladder for security reasons (handling invalid requests)
        if city_geodata:

            # make meteo api call for weather of past 5 days
            weather_data: dict = fetch_weather_data(city_geodata)
            
            if weather_data:

                # current date for vertical red line later
                today = datetime.datetime.now().date()

                # pandas df
                df = process_weather_data(weather_data)

                # plot
                plt.figure(figsize=(10, 6))
                plt.plot(df["Date"], df["Temperature"], linestyle="-", color="b")
                plt.title(f"Weather forecast {city}")
                plt.xlabel("date")
                plt.ylabel("Temperature (°C)")

                # vertical line
                plt.axvline(x=pd.to_datetime(today), color="r", linestyle=":", label="today")

                plt.xticks(rotation=45)
                plt.grid(True)
                plt.tight_layout()

                plt.legend()

                st.pyplot(plt)
            else:
                st.error("No weather data found.")