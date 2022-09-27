import time
import streamlit as st


def navigation_bar():
    # st.set_page_config(layout="wide")  # 设置屏幕展开方式，宽屏模式布局更好
    st.sidebar.write('FAE模式')

    add_selectbox = st.sidebar.radio(
        "模型训练界面",
        ("数据处理", "训练模型", "预测数据")
    )

    if add_selectbox == '数据处理':
        preparing()
    elif add_selectbox == '训练模型':
        train()
    elif add_selectbox == '预测数据':
        predict()

    return add_selectbox

def preparing():
    with st.sidebar:
        option = st.selectbox(
                    'New a project',
                    ('CNN', 'Segment'))
        if option == "CNN":
            st.subheader('Step 1: augment')
            if st.button('begin', key='button3'):
                my_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
                    time.sleep(0.5)
                    my_bar.empty()
        else :
        # 数据处理第一步
            st.subheader('Step 1: augment')
            if st.button('begin', key='button4'):
                my_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
                time.sleep(0.5)
                my_bar.empty()

                # 数据处理第二步
            st.subheader('Step 2: aug to coco')
            if st.button('begin', key='button5'):
                my_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
                time.sleep(0.5)
                my_bar.empty()
        # 数据处理第三步
            st.subheader('Step 3: create dataset')
            if st.button('begin', key='button6'):
                my_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
                time.sleep(0.5)
                my_bar.empty()
def train():
    with st.sidebar:
        cols1, cols2 = st.columns(2)
        cols1.button('begin')
        cols2.button('stop')
        st.write('参数设置')
def predict():
    with st.sidebar:
        st.write('测试集')
def setup(name: str):
    navigation_bar()

