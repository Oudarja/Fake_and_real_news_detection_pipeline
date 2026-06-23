import streamlit as st
import requests

# URL of your FastAPI backend
API_URL = "http://127.0.0.1:9000/response"

st.title("Fake News Detection")
st.write("Enter the news title and description to check if it's Real or Fake.")

# Input field
text = st.text_area("News Text")

# Use a spinner to indicate loading
if st.button("Check News"):
    if not text:
        st.warning("Please enter the news text.")
    else:
        with st.spinner("Checking news... please wait"):
            try:
                response = requests.post(API_URL, json={"text": text})
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Prediction: {result}")
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Failed to connect to API: {e}")
