#the streamlit dashboard code
#loads game data from data.json
# uses pandas to process and prepare the data 
# makes charts and tables from Streamlit
import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from fetch_steam_data import fetch_all_data

print(st.secrets['STEAM_API_KEY'])
st.set_page_config(page_title="Steam Game Analytics", layout="wide")
st.title(" Steam Data Dashboard")
user_input = st.text_input("Enter user name or Steam ID")


if st.button("Fetch Stats"):
    try:
        data = fetch_all_data(user_input)
        st.json(data)
    except Exception as e: 
        st.error(str(e))


API_KEY = os.getenv("STEAM_API_KEY")
st.write("Method 1 (getenv):", API_KEY is not None)

#loads cached data
if not os.path.exists("data.json"):
    st.error("No data json found. Run fetch_steam_data.py first")
    st.stop()
def extract_steam_data(data):
    """Extract all steam data from the JSON structure""" 
    result = {
        'steam_id': data.get('steam_id', 'unknown'),
        'profile': None,
        'games': [],
        'recent_games': [],
        'friends': [],
        'global_achievements': {},
        'player_achievements': {}
    }
    if 'profile' in data and 'response' in data['profile']:
        players = data['profile']['response'].get('players', [])
        if players:
            result['profile'] = players[0]
    if 'owned_games' in data and 'response' in data['owned_games']:
        result['games'] = data['owned_games']['response'].get('games',[])
    
    if 'recently_played' in data and 'repsonse' in data['recently_played']:
        result['result_games'] = data['recently_played']['response'].get('games',[])
    
    if 'friends' in data and 'friendslist' in data['friends']:
        result['friends'] = data['friends']['friendlist'].get('friends',[])
    
    result['global_achievements'] = data.get('global_achievements', {})
    result['player_achievements'] = data.get('player_achievements', {})
    return result 

with open("data.json", "r") as f:
    data = json.load(f)
steam_data = extract_steam_data(data)

#where you access by convienence
profile = steam_data['profile']
games = steam_data['games']
friends = steam_data['friends']


if not games:
    st.warning("No games found, make sure that your profile is public and that you play something. blah blajh blah")
else: 
    #convert list to DataFrame
    df = pd.DataFrame(games)

    df["playtime_hours"] 






























