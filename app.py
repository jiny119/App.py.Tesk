import streamlit as st
from firebase_admin import credentials, initialize_app

# Firebase سیکریٹس لوڈ کریں
cred = credentials.Certificate(st.secrets["firebase"])
initialize_app(cred)

st.title("My Streamlit Firebase App")
st.write("Firebase successfully connected!")
