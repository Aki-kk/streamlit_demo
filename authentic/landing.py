import streamlit as st
import frontend.authenticator as stauth
import yaml
import os
from frontend.pages.admin import Admin
import frontend.pages.FAE as FAE
import frontend.pages.user as user
from yaml import SafeLoader

# 界面设置
st.set_page_config(
    page_title="Demo",
    page_icon="🌼",
)
# 当前文件上一级文件夹的绝对路径
path = os.path.abspath('')
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')


if st.session_state["authentication_status"]:
    level = authenticator.credentials['usernames'][username]['level']
    with st.container():
        cols1, cols2 = st.columns(2)
        cols1.write('欢迎{}!'.format(name))
        with cols2.container():
            authenticator.logout('Logout', 'main')
    if level == 1:
        admin = Admin(username)
        admin.setup()
    if level == 2:
        FAE.setup(username)
    if level == 3:
        user.setup(username)



elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')

