
import streamlit as st
import pandas as pd

# Assuming your pickle files are in the same directory as the script
tiktok_df = pd.read_pickle('tiktok.pkl')
youtube_df = pd.read_pickle('youtube.pkl')

# Display the DataFrames
st.header("DataFrames from Pickle Files")
st.dataframe(tiktok_df.head())
st.dataframe(youtube_df.head())
