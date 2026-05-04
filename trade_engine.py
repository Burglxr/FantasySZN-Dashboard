
import os
import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Fantasy Basketball Dashboard', layout='wide')

LEAGUE_ID = st.secrets.get('LEAGUE_ID', os.getenv('LEAGUE_ID', '1346878674376347648'))
BASE = 'https://api.sleeper.app/v1'

@st.cache_data(ttl=300)
def get_league_settings(league_id):
    return requests.get(f'{BASE}/league/{league_id}').json().get('scoring_settings', {})

def calculate_fantasy_points(stats, scoring_settings):
    # balldontlie stats mapped to common Sleeper stat keys
    # Adjust mapping based on your league's specific settings
    mapping = {
        'pts': stats.get('pts', 0),
        'ast': stats.get('ast', 0),
        'reb': stats.get('reb', 0),
        'stl': stats.get('stl', 0),
        'blk': stats.get('blk', 0),
        'tov': stats.get('turnover', 0)
    }
    points = 0
    for key, value in mapping.items():
        points += value * scoring_settings.get(key, 0)
    return points

# Integration helper
def evaluate_trade(player_stats_a, player_stats_b, scoring_settings):
    pts_a = calculate_fantasy_points(player_stats_a, scoring_settings)
    pts_b = calculate_fantasy_points(player_stats_b, scoring_settings)
    diff = pts_a - pts_b
    if abs(diff) < 5: return "Fair Trade"
    return "Fleeced!" if diff > 0 else "Good Trade"

st.title("Trade Analysis Module")
st.info("Ready for live stats integration using balldontlie API.")
scoring = get_league_settings(LEAGUE_ID)
st.json(scoring)
