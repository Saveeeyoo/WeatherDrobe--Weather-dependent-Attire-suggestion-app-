import requests
import streamlit as st

def get_coords(city_name):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    res = requests.get(geo_url).json()
    
    if "results" in res:
        result = res["results"][0]
        return result["latitude"], result["longitude"]
    return None, None



def main(city):
    '''print("Enter City Name:")
    city = input()'''
    # Now you can use it like this:
    lat, lon = get_coords(city)
    if lat ==None or lon == None:
        print("Invalid city name. Please try again.")
        return main()
    return lat, lon
    # Then call your weather function from the previous step!
    
def get_weather(lat, lon):
    import openmeteo_requests
    import pandas as pd

    # 1. Setup the Open-Meteo API client
    openmeteo = openmeteo_requests.Client()

    # 2. Define your parameters (Coordinates for Mumbai)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m","weather_code","precipitation_probability"],
        "hourly": "temperature_2m"
    }

    # 3. Get the data
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # 4. Print current temperature
    current = response.Current()
    temp=round(current.Variables(0).Value(), 1)
    humidity=round(current.Variables(1).Value(), 1)
    wind=round(current.Variables(2).Value(), 1)
    wmo=int(current.Variables(3).Value())
    precip=round(current.Variables(4).Value(), 1)
    '''print(f"Current temperature: {temp}°C")
    print(f"Current humidity: {humidity}%")
    print(f"Current wind speed: {wind}MPH")
    print(f"Current wmo code: {wmo}")
    print(f"Current precipitation: {precip}mm")'''
    return temp, humidity, wind, wmo, precip;

def suggest_attire(temp, humidity, wind, wmo, precip):
    
    suggestions = []
    is_raining = precip > 0.1 or (50 <= wmo <= 67) or (80 <= wmo <= 82)
    is_snowing = (71 <= wmo <= 77) or (85 <= wmo <= 86)

    if is_snowing:
        suggestions.append("Heavy winter coat, waterproof boots, and thermal socks.")
    elif is_raining:
        if wind > 25:
            suggestions.append("Heavy-duty raincoat and waterproof shoes (too windy for an umbrella).")
        else:
            suggestions.append("Rain jacket or a sturdy umbrella.")
    
    if temp < 5:
        suggestions.append("Thermal base layer, sweater, and a thick down jacket.")
    elif 5 <= temp < 15:
        suggestions.append("A light jacket or a stylish trench coat over a sweater.")
    elif 15 <= temp < 25:
        suggestions.append("A long-sleeve shirt or a light hoodie.")
    else: 
        suggestions.append("Breathable cotton T-shirt and shorts/linen trousers.")

    if humidity > 80 and temp > 25:
        suggestions.append("Note: It's humid! Stick to moisture-wicking fabrics.")
    
    if wind > 30 and temp < 15:
        suggestions.append("High wind chill: Add a windbreaker or a scarf.")

    if not suggestions:
        return "Standard casual wear should be fine!"
        
    return " | ".join(suggestions)


