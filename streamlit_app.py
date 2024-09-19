import streamlit as st
import requests

# Flask API URL (update with your actual deployed API URL)
API_BASE_URL = "http://127.0.0.1:5000"  # Change this to your deployed Flask API URL

# Title of the app
st.title("User Management App")

# Check if user is logged in
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# If the user is logged in, show the main app interface
if st.session_state['logged_in']:
    st.header("Welcome to the User Management Dashboard")

    # Fetch users section
    st.subheader("Get All Users")
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    if st.button("Fetch Users"):
        try:
            response = requests.get(f"{API_BASE_URL}/user/get_users", headers=headers)
            if response.status_code == 200:
                users = response.json()
                st.write(users)  # Display user data
            else:
                st.error("Failed to fetch users.")
        except Exception as e:
            st.error(f"Error: {e}")

    # Add new user section
    st.subheader("Add New User")
    new_user_name = st.text_input("New User Name")
    new_user_email = st.text_input("New User Email")
    new_user_password = st.text_input("New User Password", type="password")

    if st.button("Add User"):
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

    # Logout button
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

# If the user is not logged in, show the login page
else:
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        login_data = {"email": email, "password": password}

        try:
            response = requests.post(f"{API_BASE_URL}/auth/token", json=login_data)
            if response.status_code == 200:
                token_data = response.json()
                st.session_state.access_token = token_data['access_token']
                st.session_state['logged_in'] = True
                st.experimental_rerun()  # Reload the page to update the session state
            else:
                st.error("Login failed!")
        except Exception as e:
            st.error(f"Error: {e}")
