import streamlit as st
from weathernot import get_weather, suggest_attire ,get_coords

if "choices" not in st.session_state:
    st.session_state.choices = []

st.title("weather attire advisor")
st.write("Enter a city name to get current weather conditions and attire suggestions.")
city = st.text_input("City Name", key="city_input")
if len(city) >= 3:
    st.session_state.choices = get_coords(city)
    
selected = st.selectbox(
"Choose location",
st.session_state.choices,
index=None,
placeholder="Choose a location",
format_func=lambda r: f"{r['name']}, {r.get('admin1', '')}, {r['country']}"
)

if selected:
   lat = selected["latitude"]
   lon = selected["longitude"]
   if lat is None or lon is None:
        st.error("Invalid city name. Please try again.")
   else:
        temp, humidity, wind, wmo, precip = get_weather(lat,lon)
        st.write(f"Current temperature: {temp}°C")
        st.write(f"Current humidity: {humidity}%") 
        st.write(f"Current wind speed: {wind}MPH")
        st.write(f"Current wmo code: {wmo}")
        st.write(f"Current precipitation: {precip}mm")
        outfit_advice = suggest_attire(temp, humidity, wind, wmo, precip)
        st.success(f"Weather Advice: {outfit_advice}")
        
