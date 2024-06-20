import streamlit as st
import requests
import time
# import subprocess
from utils import *

# Function to start the Flask server with a specified port
# def start_flask_server(port):
    # server_process = subprocess.Popen(["python", "flask_server.py", get_local_port()])
    # return server_process

st.set_page_config(page_title="挑战信息")

# URL of the Flask server
FLASK_SERVER_URL = f"http://localhost:{get_local_ip()}/fetch_info"

# Initialize session state
if 'new_info' not in st.session_state:
    st.session_state.new_info = None
if 'last_checked' not in st.session_state:
    st.session_state.last_checked = 0

# Function to check for new challenge info
def check_for_new_info():
    try:
        response = requests.get(FLASK_SERVER_URL)
        if response.status_code == 200:
            info = response.json().get("info")
            if info:
                st.session_state.new_info = info
    except requests.RequestException:
        st.write("Error connecting to the server")

# Check for new info every 5 seconds
if time.time() - st.session_state.last_checked > 5:
    check_for_new_info()
    st.session_state.last_checked = time.time()

# Sidebar for navigation
st.sidebar.title("Navigation")
pages = ["Home", "Challenge Info"]
page = st.sidebar.radio("Go to", pages)

# Indicator for new challenge info
if st.session_state.new_info and page != "Challenge Info":
    st.sidebar.markdown(f"### Challenge Info 🔴")

# Main page content
if page == "Home":
    st.title("Home")
    st.write("Welcome to the Challenge Info Viewer!")
elif page == "Challenge Info":
    st.title("Challenge Info")
    if st.session_state.new_info:
        st.write(f"New challenge info received: {st.session_state.new_info}")
        # Clear the new info indicator after viewing
        st.session_state.new_info = None
    else:
        st.write("No new challenge info.")
