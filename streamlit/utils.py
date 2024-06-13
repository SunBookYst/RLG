import os
import base64
import re

import streamlit as st
import hashlib

def md5_encrypt(password):
    # 创建一个 MD5 hash 对象
    md5_hash = hashlib.md5()
    
    # 更新 hash 对象，传入需要加密的密码（需要编码为字节）
    md5_hash.update(password.encode('utf-8'))
    
    # 获取加密后的十六进制字符串
    encrypted_password = md5_hash.hexdigest()
    
    return encrypted_password


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

def disable_sidebar():
    '''
    在等待系统交互的时候禁用侧边切换，以避免发生一些不可知的错误
    '''
    st.sidebar.markdown("<style>div[role='tablist'] {pointer-events: none;}</style>", unsafe_allow_html=True)


def enable_sidebar():
    '''
    系统交互结束后的时候重新启用侧边切换
    '''
    st.sidebar.markdown("<style>div[role='tablist'] {pointer-events: auto;}</style>", unsafe_allow_html=True)


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

url = "http://127.0.0.1:9981/"
ST_PATH = os.path.split(os.path.realpath(__file__))[0]