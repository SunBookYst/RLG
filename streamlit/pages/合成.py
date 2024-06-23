import streamlit as st
import requests

from utils import *


play_music()

# 定义一个映射表，将显示的文本映射到整数值
options = {
    '凤羽': 0,
    '龙眼': 1
}


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


if not st.session_state['logged_in']:
    st.write("尊敬的勇士，请先表明身份！")
    st.page_link("主页.py", label="Go to login")
else:
    selected_text = st.selectbox(
        'Pick a mode',
        list(options.keys())
    )
    # 根据选择的文本，从映射表中获取实际的整数值
    material = options[selected_text]
    num = st.text_input('Input')
    description = st.text_input('description')
    if st.button("craft"):
        output = craft(material, num, description)
        st.write(output)

while True:
    if st.session_state["logged_in"]:
        refresh(st.session_state["username"])
    time.sleep(5)