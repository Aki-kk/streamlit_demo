import time

import pandas as pd
import streamlit as st
import yaml
from PIL import Image
import numpy as np
from yaml import SafeLoader

pre_stop = 0
train_begin = 0

class Admin:
    def __init__(self, username: str):
        self.disable = False    # button禁用标志位
        with open('E:/ws/project1/authentic/frontend/config2.yaml') as file:
            self.config = yaml.load(file, Loader=SafeLoader)
            self.credentials = self.config['credentials']
        self.credentials['usernames'] = {key.lower(): value for key, value in self.credentials['usernames'].items()}
        self.username = username
        self.project = self.credentials['usernames'][self.username]['project']

    def navigation_bar(self):
        st.sidebar.write('⭐管理员模式')

        add_selectbox = st.sidebar.radio(
            "模型训练界面",
            ("数据处理", "训练模型", "预测数据")
        )
        if add_selectbox == '数据处理':
            self.preparing()
        elif add_selectbox == '训练模型':
            self.train()
        elif add_selectbox == '预测数据':
            self.predict()
        return add_selectbox

    def preparing(self):
        # 按键信号初始化
        step1 = 0
        with st.sidebar:
            st.write('───────选择工程────────')
            # new一个工程
            option1 = st.selectbox(
                'New a project',
                ('CNN', 'Segment'),
                key='slx1')
            name = st.text_input('输入名称')
            #request
            Sure = st.button('确定')
            if Sure:
                if option1 == 'CNN':
                    if name not in self.project:
                        self.config['credentials']['usernames'][self.username] = {'project': self.project+list(name.split())}
                        self.project = self.project+list(name.split())
                        with open("E:/ws/project1/authentic/frontend/config2.yaml", "w", encoding="utf-8") as file:
                            yaml.dump(self.config, file)
                    else:
                        st.error('文件名不能重复！')
                else:
                    self.credentials['usernames'][self.username] = {'project': self.project+name}
            option2 = st.selectbox(
                'Open a project',
                self.project,
                key='slx2')
            st.write('───────数据处理────────')
            if st.button('begin', key='button3', disabled=self.disable):
                my_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
                    self.disable = True
                time.sleep(0.5)
                my_bar.empty()
            self.disable = True

        st.write('──────────────────────────结果预览──────────────────────────')
        st.slider
        if pre_stop == 1:
            # 显示图片处理结果
            pic_num = st.slider('查看结果', 1, 3, 1)
            image = Image.open('E:/dataset/001_test/' + str(pic_num) + '.jpeg')
            st.image(image)

    def train(self):
        with st.sidebar:
            st.write('────────●─●─────────')
            cols1, cols2 = st.columns(2)
            if cols1.button('begin'):
                # request
                my_bar = st.progress(0)
                global train_begin
                train_begin = 1
                for percent_complete in range(100):
                    if self.stop != 1:
                        time.sleep(0.01)
                        my_bar.progress(percent_complete + 1)
                    else:
                        break
                time.sleep(0.5)
                # my_bar.empty()
            if cols2.button('stop'):
                # request
                stop = 1
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
            st.write('───────训练结果────────')
            # request
            train_acc = 0.0
            st.write('train accuracy is: ', train_acc)
            # request
            val_acc = 0.0
            st.write('validation accuracy is: ', val_acc)
        # 动态绘制loss曲线
        st.write('──────────────────────────loss曲线──────────────────────────')
        if train_begin == 1:
            self.draw_loss()

    def predict(self):
        with st.sidebar:
            st.write('───────测试集─────────')
            if st.button('begin'):
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
            st.write('──────自定义图片───────')
            st.button('select')
            # request
            result = 'OK'
            st.write('result: ', result)

    def draw_loss(self):
        # request
        train_loss_list = np.array([])
        val_loss_list = np.array([])
        train_loss = 0.1
        val_loss = 0.2
        train_loss_list = np.append(train_loss_list, train_loss)
        val_loss_list = np.append(val_loss_list, val_loss)
        chart_data = pd.DataFrame(
            np.array(list(zip(train_loss_list, val_loss_list))),
            columns=['train loss', 'val loss']
        )
        chart = st.line_chart(chart_data)
        for i in range(1, 10):
            train_loss = np.random.randn(1)
            val_loss = np.random.randn(1)
            new_data = pd.DataFrame(
                np.array(list(zip(train_loss, val_loss))),
                columns=['train loss', 'val loss']
            )
            chart.add_rows(new_data)
            # last_rows = new_rows
            time.sleep(1)


    def setup(self):
        self.navigation_bar()


