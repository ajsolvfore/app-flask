import streamlit as st
import requests

# Flask API URL (update with your actual deployed API URL)
API_BASE_URL = "https://app-flask-qlkhouuzfgemcgdrgc4dfb.streamlit.app/"  # Change this to your deployed Flask API URL

st.title("User Management App")

# Login and get JWT token
st.header("Login")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    login_data = {"email": email, "password": password}
    
    try:
        # Send POST request to Flask API for login
        response = requests.post(f"{API_BASE_URL}/auth/token", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            st.success(f"Logged in! Access Token: {token_data['access_token']}")
            st.session_state.access_token = token_data['access_token']  # Save the token
        else:
            st.error("Login failed!")
    except Exception as e:
        st.error(f"Error: {e}")

# Fetch users (only if logged in)
if 'access_token' in st.session_state:
    st.header("Get All Users")
    
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    if st.button("Fetch Users"):
        try:
            response = requests.get(f"{API_BASE_URL}/user/get_users", headers=headers)
            if response.status_code == 200:
                users = response.json()
                st.write(users)  # Display user data in Streamlit
            else:
                st.error("Failed to fetch users.")
        except Exception as e:
            st.error(f"Error: {e}")

# Add new user
st.header("Add New User")
new_user_name = st.text_input("New User Name")
new_user_email = st.text_input("New User Email")
new_user_password = st.text_input("New User Password", type="password")

if st.button("Add User"):
    if 'access_token' in st.session_state:
        new_user_data = {
            "name": new_user_name,
            "email": new_user_email,
            "password": new_user_password
        }
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        try:
            response = requests.post(f"{API_BASE_URL}/user/add", json=new_user_data, headers=headers)
            if response.status_code == 201:
                st.success("User added successfully!")
            else:
                st.error("Failed to add user.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please log in to add a user.")
