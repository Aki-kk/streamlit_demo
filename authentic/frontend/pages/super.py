import streamlit as st
import yaml
import os
from yaml import SafeLoader


class Super:
    def __init__(self):
        path = os.path.abspath('')
        # 读取table 1
        with open('E:/ws/project1/config.yaml') as file:
            self.config1 = yaml.load(file, Loader=SafeLoader)
        self.credentials1 = self.config1['credentials']
        self.credentials1['usernames'] = {key.lower(): value for key, value in self.credentials1['usernames'].items()}
        self.username1 = self.credentials1['usernames']
        # 读取table2
        path = os.path.abspath('')
        with open('E:/ws/project1/authentic/frontend/config2.yaml') as file:
            self.config2 = yaml.load(file, Loader=SafeLoader)
            self.credentials2 = self.config2['credentials']
        self.credentials2['usernames'] = {key.lower(): value for key, value in self.credentials2['usernames'].items()}

    def register(self):
        register_user_form = st.form('Register user')
        register_user_form.subheader('Register')
        new_email = register_user_form.text_input('Email')
        new_username = register_user_form.text_input('Username').lower()
        new_name = register_user_form.text_input('Name')
        new_password = register_user_form.text_input('Password', type='password')
        new_password_repeat = register_user_form.text_input('Repeat password', type='password')
        new_level = register_user_form.selectbox('选择权限:', (1, 2, 3, 4))
        if register_user_form.form_submit_button('Register'):
            if len(new_email) and len(new_username) and len(new_name) and len(new_password) > 0:
                if new_username not in self.credentials1['usernames']:
                    if new_password == new_password_repeat:
                        self.config1['credentials']['usernames'][new_username] = {'name': new_name,
                            'password': int(new_password), 'email': new_email, 'level': new_level}
                        with open("E:/ws/project1/config.yaml", "w", encoding="utf-8") as file:
                            yaml.dump(self.config1, file)
                        st.success('注册成功！')
                    else:
                        st.warning("前后输入密码不一致！")
                else:
                    st.warning("用户名已存在")
            else:
                st.warning("请输入有效信息")

    def main_page(self):
        st.write('hello')
    def setup(self):
        with st.expander('注册'):
            self.register()
        self.main_page()

