import time

import streamlit as st
import requests

from utils import *

def get_player_info():
    response = requests.get(url + 'status', json={
        'role': st.session_state['username']
    })

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.write("Error: Unable to select this task.")


if not st.session_state['logged_in']:
    st.write("尊敬的勇士，请先表明身份！")
    st.page_link("home_page.py", label="Go to login")
else:
    attribute = get_player_info()
    if st.button('refresh'):
        st.rerun()

    st.write(attribute)

while True:
    if st.session_state["logged_in"]:
        refresh(st.session_state["username"])
    time.sleep(5)
