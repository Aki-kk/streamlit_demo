import time
import streamlit as st

def side():
    with st.sidebar:
        st.write('用户模式')

def main_page(name: str):
    st.subheader('预测结果展示')
    st.write("项目基本信息")
    st.text('名称:')
    st.text('所属人:{}'.format(name))
def setup(name: str):
    side()
    main_page(name)
