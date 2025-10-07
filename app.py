import streamlit as st
from dotenv import load_dotenv
import os
from apputil import Genius

load_dotenv()
access= os.getenv("ACCESS_TOKEN")
genius = Genius(access_token=access)
st.write(
'''
# Week 6: [GENIUS API]

''')

st.set_page_config(page_title="Genius Artist Search", layout="centered")
st.title("Genius Artist Search")


st.subheader("Search for an Artist")
artist_name = st.text_input("Enter Artist Name: ", placeholder="Radiohead")

if st.button("Search"):
    if artist_name.strip():
        try:
            artist_data = genius.get_artist(artist_name)
            artist_info = artist_data.get("response", {}).get("artist", {})
            artist_name_found = artist_info.get("name")

            if artist_name_found:
                st.success(f"Artist Found: {artist_name_found}")
                st.json(artist_info)
            else:
                st.warning("Artist found, name not available.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid artist name.")

st.subheader("Search for Multiple Artists")
artist_names = st.text_area("Enter Artist Names (one per line): ", placeholder="Radiohead\nAdele\nDrake")
if st.button("Search Multiple"):
    names_list = [name.strip() for name in artist_names.split("\n") if name.strip()]
    if names_list:
        df = genius.get_artists(names_list)
        st.dataframe(df)
    else:
        st.warning("Please enter at least one artist name.")
    
