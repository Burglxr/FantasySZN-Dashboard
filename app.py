import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Fantasy Basketball Dashboard', layout='wide')

# Use environment variable for the League ID
LEAGUE_ID = st.secrets.get('LEAGUE_ID', os.getenv('LEAGUE_ID', '1346878674376347648'))
BASE = 'https://api.sleeper.app/v1'

@st.cache_data(ttl=300)
def get_json(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=300)
def load_league_data(league_id):
    league = get_json(f'{BASE}/league/{league_id}')
    users = get_json(f'{BASE}/league/{league_id}/users')
    rosters = get_json(f'{BASE}/league/{league_id}/rosters')
    transactions = []
    # Fetching transaction history (assuming up to 24 weeks)
    for week in range(1, 25):
        transactions.extend(get_json(f'{BASE}/league/{league_id}/transactions/{week}'))
    return league, users, rosters, transactions

league, users, rosters, transactions = load_league_data(LEAGUE_ID)
user_names = {u.get('user_id'): u.get('display_name') or u.get('username') or 'Unknown' for u in users}

st.title(f"{league.get('name', 'Fantasy Basketball')} Dashboard")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Overview', 'Rosters', 'Matchups', 'History', 'Transactions', 'Settings'])

with tab1:
    st.subheader('League Overview')
    league_df = pd.DataFrame([
        {'Roster': r.get('roster_id'), 'Manager': user_names.get(r.get('owner_id'), 'Unknown'), 'Players': len(r.get('players', []) or [])}
        for r in rosters
    ]).sort_values('Roster')
    st.dataframe(league_df, use_container_width=True, hide_index=True)

with tab4:
    st.subheader('League History')
    hist_data = [{'Season': 2025, 'Champion': 'Asbury95', 'Runner-up': 'SamuelTheGoat96', '3rd': 'Zackarymichel', '4th': 'blumthal', 'Note': 'King of Toilet Bowl: RVilla90'}]
    st.table(pd.DataFrame(hist_data))

with tab5:
    st.subheader('Transactions & Trades')
    trades = [t for t in transactions if t.get('type') == 'trade']
    for trade in trades[:10]:
        st.divider()
        st.write(f"Trade ID: {trade.get('transaction_id')}")
        if st.button(f'Analyze Trade {trade.get("transaction_id")}', key=trade.get('transaction_id')):
            st.warning('AI Trade Analysis requires stats integration. Plug in a league scoring API next!')
