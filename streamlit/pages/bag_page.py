import streamlit as st
import requests
import time

url = "http://127.0.0.1:5000/"


def get_bag_info():
    response = requests.get(url + 'bag', json={
        'role': st.session_state['username']
    })

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.write("Error: Unable to select this task.")


def get_skill_info():
    response = requests.get(url + 'skill', json={
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
    equipment = get_bag_info()
    skill = get_skill_info()
    if st.button('refresh'):
        st.rerun()

    st.write("装备栏")
    st.write(equipment)
    st.write("技能槽")
    st.write(skill)
