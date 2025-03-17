import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
import json

# Firebase Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")  # Replace with your Firebase JSON file
    firebase_admin.initialize_app(cred)

db = firestore.client()

# User Authentication
def signup(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        st.success("Account created successfully! Please login.")
    except:
        st.error("Signup failed. Try a different email.")

def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        st.session_state["user"] = email
        st.success("Login Successful!")
    except:
        st.error("Invalid email or password.")

# Function to Add Coins
def add_coins(user_email, coins):
    user_ref = db.collection("users").document(user_email)
    user_data = user_ref.get()
    if user_data.exists:
        current_coins = user_data.to_dict().get("coins", 0)
        user_ref.update({"coins": current_coins + coins})
    else:
        user_ref.set({"coins": coins, "referrals": 0, "clicks": 0})

# Function to Handle Withdrawal
def withdraw_request(user_email, method, amount):
    user_ref = db.collection("users").document(user_email)
    user_data = user_ref.get()
    
    if user_data.exists:
        data = user_data.to_dict()
        if data["coins"] >= amount and data["referrals"] >= 10 and data["clicks"] >= 5:
            db.collection("withdraw_requests").add({
                "email": user_email,
                "method": method,
                "amount": amount,
                "status": "Pending"
            })
            user_ref.update({"coins": data["coins"] - amount})
            st.success("Withdrawal request submitted!")
        else:
            st.error("You need at least 10 referrals and 5 clicks to withdraw.")
    else:
        st.error("User not found!")

# UI
st.title("🔥 Tasking WebApp 🔥")
st.sidebar.header("User Panel")

if "user" not in st.session_state:
    option = st.sidebar.radio("Login/Signup", ["Login", "Signup"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if option == "Signup" and st.sidebar.button("Create Account"):
        signup(email, password)

    if option == "Login" and st.sidebar.button("Login"):
        login(email, password)

else:
    user_email = st.session_state["user"]
    st.sidebar.success(f"Logged in as {user_email}")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.pop("user"))

    tab1, tab2, tab3 = st.tabs(["🏆 Tasks", "💰 Withdraw", "👥 Referrals"])

    with tab1:
        st.header("Complete Tasks to Earn Coins!")
        if st.button("Watch Ad"):
            add_coins(user_email, 5)
            st.success("5 Coins Added!")

        if st.button("Install App"):
            add_coins(user_email, 5)
            st.success("5 Coins Added!")

        if st.button("Take Survey"):
            add_coins(user_email, 5)
            st.success("5 Coins Added!")

        if st.button("Play Game"):
            add_coins(user_email, 5)
            st.success("5 Coins Added!")

    with tab2:
        st.header("Withdraw Your Earnings")
        method = st.selectbox("Select Payment Method", ["JazzCash", "EasyPaisa", "Payoneer", "PayPal"])
        amount = st.number_input("Enter Amount (Min: 15000)", min_value=15000, step=500)
        if st.button("Withdraw"):
            withdraw_request(user_email, method, amount)

    with tab3:
        st.header("Referral System")
        st.write("Refer 10 friends and get extra rewards!")
        referral_link = f"https://yourapp.com/signup?ref={user_email}"
        st.code(referral_link)
        st.button("Copy Link", on_click=lambda: st.success("Referral Link Copied!"))
st.sidebar.button("Share App", on_click=lambda: st.success("Share on Social Media!"))
