import streamlit as st
import requests

url = "http://127.0.0.1:5000/"


# response = bs.craft_items(data["role"], data["mode"], data["num"], data["des"])
def craft(mode, num, des):
    response = requests.get(url + 'merge', json={
        'role': st.session_state['username'],
        'mode': mode,
        'num': int(num),
        'des': des
    })

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.write("Error: Unable to select this task.")


material = st.selectbox(
                'Pick a mode',
                [0, 1],
            )
num = st.text_input('Input')
description = st.text_input('description')
if st.button("craft"):
    output = craft(material, num, description)
    st.write(output)
