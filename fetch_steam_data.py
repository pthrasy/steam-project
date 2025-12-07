#pulls the data from steam
import os 
import requests
import json

API_KEY = os.getenv("STEAM_API_KEY")  # set in Render later

if not API_KEY:
    # raise ValueError("Missing STEAM_API_KEY environment variable")

def vanity_name_def(vanity_name):
    #sees if steam id is there
    #if the 17 digit steam id, return it

    if vanity_name.isdigit() and len(vanity_name) == 17: 
        return vanity_name
    #converts steam name into steam id
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {
         "key": API_KEY,
         "vanityurl": vanity_name
         }

    response = requests.get(url, params=params).json()
    result = response.get("response", {})
    
    if result.get("success") == 1:
        return result.get("steamid")
    else:
        print("Failed to resolve vanity name:", result)
        return None


def fetch_owned_games(steam_id):
  #fetches data from api

    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1"
    params = {
       "key" : API_KEY, 
       "steamid": steam_id,
       "format": "json",
       "include_appinfo": True,
       "include_played_free_games": True
    }
     
    response = requests.get(url, params=params)
    print("Status:", response.status_code)

    print("Steam ID being used:", repr(steam_id))
    print("These are the games that are owned")

    try:
        data = response.json()
        print("Parsed:", data)
        return data
    except Exception as e:
        print("Error parsing JSON:", e)
        return None

    
def fetch_recently_played(steam_id):
  #fetches data from api

    url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1"
    params = {
       "key" : API_KEY, 
       "steamid": steam_id,
       "format": "json"
    }
    response = requests.get(url, params=params)
    print("Status:", response.status_code)

    print("Steam ID being used:", repr(steam_id))
    print("These are the games recently played")
    
    try:
        data = response.json()
        print("Parsed:", data)
        return data
    except Exception as e:
        print("Error parsing JSON:", e)
        return None

    
def fetch_player_summary(steam_id):
    #fetches data for player summary

    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": API_KEY, 
        "steamids": steam_id
     }
    response = requests.get(url, params=params)
    print("Status:", response.status_code)

    print("Steam ID being used:", repr(steam_id))
    print("These are the details of the profile")

    try:
        data = response.json()
        print("Parsed:", data)
        return data
    except Exception as e:
        print("Error parsing JSON:", e)
        return None



def fetch_friends_list(steam_id):
    #fetches data for friends list
    url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v1"
    params = {
        "key": API_KEY, 
        "steamid": steam_id,
        "relationship":"friend"
     }
    response = requests.get(url, params=params)
    print("Status:", response.status_code)

    print("Steam ID being used:", repr(steam_id))
    print("These are the friends of the profile")


    try:
        data = response.json()
        print("Parsed:", data)
        return data
    except Exception as e:
        print("Error parsing JSON:", e)
        return None

def fetch_player_achievements(appid, steam_id):
    #fetches player achievements 
    url = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "appid" : appid
    }
    response = requests.get(url, params=params)

    print("These are the player achievements")
    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")
    print(response.text)
    print("Steam ID being used:", repr(steam_id))
 
    
    if response.status_code == 200:
            try:
                data = response.json()
                print("Parsed JSON:", data)
                return data
            except Exception as e:
                print("JSON parsing failed:", e)
    else:
        print(f"Request failed for appid {appid}")

# #might add in another for looking up a game and seeing what achivements a user got
#https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/

def fetch_global_achievements(appid):
    url = f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/?gameid={appid}"  
    params = {
        "key": API_KEY,
        "gameid" : appid
    }
    response = requests.get(url)
    print("Status Code:", response.status_code)
    print(f"This is the global achievement")

    if response.status_code == 200:
            try:
                data = response.json()
                print("Parsed JSON:", data)
                return data
            except Exception as e:
                print("JSON parsing failed:", e)
    else:
        print(f"Request failed for appid {appid}")





def fetch_all_data(vanity_name):
    steam_id = vanity_name_def(vanity_name)
    
    #user level data
    profile = fetch_player_summary(steam_id)
    owned_games = fetch_owned_games(steam_id)
    recently_played = fetch_recently_played(steam_id)
    friends = fetch_friends_list(steam_id)

    #Global achivements data for all owned games
    player_achievements = {}
    global_achievements = {}

#debugs stuff
    
    game_count = owned_games.get("response", {}).get("game_count")
    games = owned_games.get("response", {}).get("games", [])
    # player_info = profile.get("response", {}).get("players", [])# Debug line
    # recent_games = recently_played.get("response", {}).get("games", [])# Debug line
    # friend_ids = friends.get("friendslist", {}).get("friends", [])# Debug line


    print(f"Games: {games}")
    # print(f"friend_ids: {friend_ids}")  # Debug line
    # print(f"player_info: {player_info}")  # Debug line


    for game in games:
        appid = game['appid']
        print(f"Processing appid: {appid}")  # Debug line

        try:
            achievements = fetch_global_achievements(appid)
            if not achievements:
                print(f"No data returned for appid {appid}")
                global_achievements[appid] = None
            else:
                global_achievements[appid] = achievements
#had problem where couldnt process player achivements FIXED needed to give achivements its own if else statement
            p_achievements = fetch_player_achievements(appid, steam_id)
            if not p_achievements:
                print(f"No data returned for appid {appid}")
                player_achievements[appid] = None
            else:
                player_achievements[appid] = p_achievements
            
        except Exception as e:
            print(f"Error with appid {appid}: {e}")
            global_achievements[appid] = None
            player_achievements[appid] = None

    

    data = {
        "steam_id": steam_id,
        "profile": profile, 
        "owned_games" : owned_games,
        "recently_played": recently_played,
        "friends":friends,
        "global_achievements": global_achievements,
        "player_achievements": player_achievements
    }

    return data

def save_data(data, filename="data.json"):
    """
    Saves fetched data to a JSON file.
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")
    

if __name__ == "__main__":
    vanity_name = input("Enter your Steam vanity name or steam id:")
    try:
        data = fetch_all_data(vanity_name)
        save_data(data)
        print("Steam data successfully fetched and stored.")
    except Exception as e:
        print(f"Error: {e}")


