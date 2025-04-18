import streamlit as st
import pickle as pk
import pandas as pd
import numpy as np

model = pk.load(open('rf_model.pkl', 'rb'))

feature_names = pk.load(open('feature_names.pkl', 'rb'))

st.title("Movie Revenue Prediction App")



budget = st.number_input(" Budget ($)", min_value=1000, step=10000)
runtime = st.number_input(" Runtime (minutes)", min_value=30, max_value=380, step=1)
vote_average = st.slider(" IMDb Vote Average", 0.0, 10.0, step=0.1)
vote_count = st.number_input(" Vote Count", min_value=100, max_value=14000, step=10)
popularity = st.number_input(" Popularity Score", min_value=0.0, max_value=550.0, step=0.1)
release_year = st.number_input(" Release Year", min_value=1915, step=1)
release_month = st.slider("Release Month", 1, 12, step=1)
all_genres = ['Animation', 'Adventure', 'Comedy', 'Action', 'History', 'Drama', 'Crime',
    'Fantasy', 'Science Fiction', 'Horror', 'Romance', 'Mystery', 'Thriller',
    'Documentary', 'Family', 'War', 'Western', 'Music', 'TV Movie', 'Foreign']

genre = st.selectbox("Select Primary Genre", all_genres)

genre_encoded = {f"primary_genre_{g}": 1 if g == genre else 0 for g in all_genres}

input_data = pd.DataFrame({
    "budget": [budget],
    "runtime": [runtime],
    "vote_average": [vote_average],
    "vote_count": [vote_count],
    "popularity": [popularity],
    "release_year": [release_year],
    "release_month": [release_month]
})

for col in feature_names:
    if col not in input_data.columns:
        input_data[col] = genre_encoded.get(col, 0)

input_data = input_data[feature_names]


if st.button(" Predict Revenue"):
    prediction = model.predict(input_data)[0]
    roi = (prediction - budget) / budget
    profit = prediction - budget 
    st.subheader("Prediction Result")
    st.success(f"Predicted Revenue: ${prediction:,.2f}")
    st.info(f"ROI (Return on Investment): {roi:.2f}")
    st.info(f"Profit on Investment: ${profit:.2f}")