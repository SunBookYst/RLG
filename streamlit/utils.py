import os
import base64
import re

import streamlit as st



def set_background(image_path, opacity):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})), 
                        url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def parse_message(message):
    """
    解析消息字符串，提取 role 和 text
    Args:
        message: 消息字符串，形如 "role: text"

    Returns:
        role: 角色
        text: 消息内容
    """
    match = re.match(r"([^:]+):\s*(.*)", message)
    if match:
        return match.group(1), match.group(2)
    else:
        return "系统", message

url = "http://127.0.0.1:5000/"
ST_PATH = os.path.split(os.path.realpath(__file__))[0]