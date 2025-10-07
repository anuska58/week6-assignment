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
            st.success(f"Artist Found: {artist_data.get('name')}")
            st.json(artist_data)
        except ValueError as ve:
            st.error(str(ve))
        except Exception as e:
            st.error("An error occurred while fetching artist data.")
    else:
        st.warning("Please enter an artist name.")

st.subheader("Search for Multiple Artists")
artist_names = st.text_area("Enter Artist Names (one per line): ", placeholder="Radiohead\nAdele\nDrake")
if st.button("Search Multiple"):
    names_list = [name.strip() for name in artist_names.split("\n") if name.strip()]
    if names_list:
        df = genius.get_artists(names_list)
        st.dataframe(df)
    else:
        st.warning("Please enter at least one artist name.")
        


