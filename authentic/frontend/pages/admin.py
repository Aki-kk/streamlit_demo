import os
import time
from datetime import datetime
import io

from pandas.core.frame import DataFrame
import requests
import pandas as pd
import streamlit as st
import yaml
import extra_streamlit_components as stx
from PIL import Image
import numpy as np
from yaml import SafeLoader

pre_stop = 0

class Admin:
    def __init__(self, username: str):
        # 读取config2
        path = os.path.abspath('')
        with open('E:/ws/project1/authentic/frontend/config2.yaml') as file:
            self.config = yaml.load(file, Loader=SafeLoader)
            self.credentials = self.config['credentials']
        self.credentials['usernames'] = {key.lower(): value for key, value in self.credentials['usernames'].items()}
        self.username = username
        self.cnn_project = self.credentials['usernames'][self.username]['project']['CNN']
        self.seg_project = self.credentials['usernames'][self.username]['project']['Segment']

        # 读取config3
        with open('E:/ws/project1/authentic/frontend/config3.yaml') as file:
            self.config3 = yaml.load(file, Loader=SafeLoader)
            self.project = self.config3['Project']
        self.project['name'] = {key.lower(): value for key, value in self.project['name'].items()}

        # 标志位初始化
        self.trainon = 0
        # 缓存初始化
        self.cookie_manager = stx.CookieManager('chart')
        if 'trainon' not in st.session_state:
            st.session_state.trainon = 0
        if 'pjtname' not in st.session_state:
            st.session_state.pjtname = 'a'
        if 'data' not in st.session_state:
            new_data = pd.DataFrame(
                np.array([[0, 0]]),
                columns=['train loss', 'val loss']
            )
            st.session_state.data = new_data
        if 'train_acc' not in st.session_state:
            st.session_state.train_acc = 0
        if 'val_acc' not in st.session_state:
            st.session_state.val_acc = 0
        if 'test_acc' not in st.session_state:
            st.session_state.test_acc = 0
        # if 'uploaded_img' not in st.session_state:
        #     st.session_state.uploaded_img = 0
        # 变量初始化
        self.train_loss_list = np.array([])
        self.val_loss_list = np.array([])
        self.train_acc = 0
        self.val_acc = 0
    def navigation_bar(self):
        st.sidebar.write('⭐管理员模式')

        add_selectbox = st.sidebar.radio(
            "模型训练界面",
            ("选择工程", "数据处理", "训练模型", "预测数据")
        )
        if add_selectbox == '选择工程':
            self.selecting()
        elif add_selectbox == '数据处理':
            self.preparing()
        elif add_selectbox == '训练模型':
            self.train()
        elif add_selectbox == '预测数据':
            self.predict()
        return add_selectbox
    def selecting(self):
        with st.sidebar:
            st.write('───────选择工程────────')
            # open一个工程
            option2 = st.selectbox(
                'Choose a project',
                self.cnn_project + self.seg_project,
                key='slx2')
            cols1, cols2 = st.columns(2)
            if cols1.button('open'):
                st.session_state.pjtname = option2
                val_acc = self.project['name'][st.session_state.pjtname]['val_acc']
            if cols2.button('begin', key='button3'):
                if st.session_state.pjtname in self.project['name']:
                    my_bar = st.progress(0)
                    for percent_complete in range(100):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete + 1)
                    time.sleep(0.5)
                    my_bar.empty()
                else:
                    st.error('此工程不存在')
            # new一个工程
            st.write('───────新建工程────────')
            option1 = st.selectbox(
                'New a project',
                ('CNN', 'Segment'),
                key='slx1')
            name = st.text_input('输入名称')
            # request
            Sure = st.button('确定')
            if Sure:
                if option1 == 'CNN':
                    if name not in self.cnn_project:
                        self.config['credentials']['usernames'][self.username]['project'][
                            'CNN'] = self.cnn_project + list(name.split())
                        self.cnn_project = self.cnn_project + list(name.split())
                        with open("E:/ws/project1/authentic/frontend/config2.yaml", "w", encoding="utf-8") as file:
                            yaml.dump(self.config, file)
                    else:
                        st.error('文件名不能重复！')
                elif option1 == 'Segment':
                    if name not in self.seg_project:
                        self.config['credentials']['usernames'][self.username]['project'][
                            'Segment'] = self.seg_project + list(name.split())
                        self.seg_project = self.seg_project + list(name.split())
                        with open("E:/ws/project1/authentic/frontend/config2.yaml", "w", encoding="utf-8") as file:
                            yaml.dump(self.config, file)
                    else:
                        st.error('文件名不能重复！')
                self.config3['Project']['name'][name] = {'loss': 0, 'test_acc': 0, 'val_acc': 0}
                with open("E:/ws/project1/authentic/frontend/config3.yaml", "w", encoding="utf-8") as file:
                    yaml.dump(self.config3, file)
            # 初始化信息
        val_acc = self.project['name'][st.session_state.pjtname]['val_acc']
        test_acc = self.project['name'][st.session_state.pjtname]['test_acc']

        st.write('──────────────────────────项目信息──────────────────────────')
        st.write('项目名称：', st.session_state.pjtname)
        st.write('所属人：', self.username)
        st.write('当前验证集精确度：', val_acc)
        st.write('当前测试集精确度：', test_acc)
    def preparing(self):
        with st.sidebar:
            st.write('───────数据处理────────')
            multiple = st.text_input('输入增强倍数', '10')
            # request
            # 如果本地数据集为空，弹出警告
            # 增加上传button
            st.file_uploader("上传数据集", accept_multiple_files=True)
            st.button('begin')
            # request
        # request 查询本地有无data，若有 slide显示
        st.slider('查看数据集', 1, 10, 1)
        # 增强结束后显示
        pic_num = st.slider('查看图像增强结果', 1, 10, 1)
    def train(self):
        with st.sidebar:
            st.write('───────参数设置────────')
            cols3, cols4 = st.columns(2)
            lr = cols3.text_input('learning rate', '0.001')
            # request
            batch_size = cols4.text_input('batch size', '64')
            # request
            optimizer = st.selectbox(
                '选择优化器类型',
                ('Adam', 'RAdam', 'SGD', 'ASGD')
            )
            cols1, cols2 = st.columns(2)
            if cols1.button('begin'):
                if st.session_state.pjtname in self.project['name']:
                    requests.get(f"http://127.0.0.1:8000/train_on")
                    self.trainon = 1
                    st.session_state.trainon = 1
                    # request
                    time.sleep(1)
                else:
                    st.error('此工程不存在')
            if cols2.button('stop'):
                self.trainon = 0
                st.session_state.trainon = 0
        # 动态绘制loss曲线
        st.write('──────────────────────────loss曲线──────────────────────────')
        if st.button('clear'):
            self.cookie_manager.delete('loss')
        if self.trainon == 0:
            chart_data = pd.DataFrame(
                self.cookie_manager.get(cookie='loss'),
                index=['train loss', 'val loss']
            )
            chart = st.line_chart(chart_data.T)
            st.write(chart_data.T)
        # 画loss
        # 获取acc
        # 在config3中更改val_acc
        if st.session_state.trainon == 1:
            self.draw_loss()
            self.get_acc()
            self.config3['Project']['name'][st.session_state.pjtname]['val_acc'] = st.session_state.val_acc
            with open("E:/ws/project1/authentic/frontend/config3.yaml", "w", encoding="utf-8") as file:
                yaml.dump(self.config3, file)

        st.write('train accuracy is: ', st.session_state.train_acc)
        # request
        st.write('validation accuracy is: ', st.session_state.val_acc)
    def predict(self):
        with st.sidebar:
            st.write('───────测试集─────────')
            if st.button('begin', key=11):
                # request
                my_bar = st.progress(0)
                global train_begin
                train_begin = 1
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
                time.sleep(0.5)
            # request
            test_acc = 0.0
            st.write('train accuracy is: ', test_acc)
            uploaded_imgs = st.file_uploader("选择待检测图片", accept_multiple_files=True)

        # request 预测完毕后显示
        pic_num = st.slider('查看测试集预测结果', 1, 10, 1)
        if len(uploaded_imgs) > 1:
            # request
            num = st.slider('查看结果', 1, len(uploaded_imgs), 1)
            st.image(uploaded_imgs[num-1])
            result = 'OK'
            st.write('result is', result)
        elif len(uploaded_imgs) == 1:
            # request
            st.image(uploaded_imgs[0])
            result = 'OK'
            st.write('result is', result)
        '''
        实验 
        向后端获取图片
        '''
        if st.button('get img'):
            bytes_data = requests.get(f"http://127.0.0.1:8000/pic")
            st.image(bytes_data.content)

    def draw_loss(self):
        train_loss_list = []
        val_loss_list = []
        for i in range(10):
            loss = requests.get(f"http://127.0.0.1:8000/ask1")
            loss = loss.json()
            train_loss = loss[0]
            val_loss = loss[1]
            self.train_loss_list = np.append(self.train_loss_list, train_loss)
            train_loss_list.append(train_loss)
            self.val_loss_list = np.append(self.val_loss_list, val_loss)
            val_loss_list.append(val_loss)
            chart_data = pd.DataFrame(
                np.array(list(zip(self.train_loss_list, self.val_loss_list))),
                columns=['train loss', 'val loss']
            )
            st.session_state.data = chart_data
            chart = st.line_chart(st.session_state.data)
            time.sleep(0.5)
            chart.empty()
            # chart.line_chart(st.session_state.data)
            # 设置cookie
        self.cookie_manager.set('loss', [train_loss_list, val_loss_list],
                                expires_at=datetime(year=2025, month=2, day=2))
        st.session_state.trainon = 0

    def get_acc(self):
        train_acc = requests.get(f"http://127.0.0.1:8000/train")
        self.train_acc = train_acc.json()
        val_acc = requests.get(f"http://127.0.0.1:8000/val")
        self.val_acc = val_acc.json()

        # 训练完成后存储一次
        st.session_state.train_acc = self.train_acc
        st.session_state.val_acc = self.val_acc
    def setup(self):
        self.navigation_bar()





