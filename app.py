#the streamlit dashboard code
#loads game data from data.json
# uses pandas to process and prepare the data 
# makes charts and tables from Streamlit

import json
import pandas as pd
import streamlit as st
import plotly.express as px
import os
from fetch_steam_data import fetch_all_data

st.set_page_config(page_title="Steam Game Analytics", layout="wide")
st.title(" Steam Data Dashboard")
user_input = st.text_input("Enter user name or Steam ID")
import osAPI_KEY = os.getenv("STEAM_API_KEY")
API_KEY = os.getenv("STEAM_API_KEY")
st.write("API loaded:", API_KEY is not None)
if not API_KEY:
    st.error("Missing Steam API key. Go to Render → Your Service → Environment and add STEAM_API_KEY.")
    st.stop()
    
if st.button("Fetch Stats"):
    try:
        data = fetch_all_data(user_input)
        st.json(data)
    except Exception as e: 
        st.error(str(e))


API_KEY = os.getenv("STEAM_API_KEY")

st.write("API loaded:", API_KEY is not None)

if not API_KEY:
    st.error("Missing Steam API key. Check environment variables.")
    st.stop()
#loads cached data
if not os.path.exists("data.json"):
    st.error("No data json found. Run fetch_steam_data.py first")
    st.stop()

with open("data.json", "r") as f:
    data = json.load(f)

games = data['response'].get("games", [])

if not games:
    st.warning("No games found, make sure that your profile is public and that you play something.")
else: 
    #convert list to DataFrame
    df = pd.DataFrame(games)

    df["playtime_hours"] 








