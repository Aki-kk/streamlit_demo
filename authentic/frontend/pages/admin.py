import os
import time
from datetime import datetime, timedelta
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
        # ------标志位初始化
        self.trainon = 0
        # ------缓存初始化
        self.cookie_manager =self.get_manager()
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
        if 'train_loss_list' not in st.session_state:
            st.session_state.train_loss_list = []
        if 'val_loss_list' not in st.session_state:
            st.session_state.val_loss_list = []
        # if 'uploaded_img' not in st.session_state:
        #     st.session_state.uploaded_img = 0
        # ------变量初始化
        # self.url = 'http://10.110.77.190:8000'
        self.url = 'http://127.0.0.1:8000'
        self.path = 'E:/ws/project1'
        self.train_loss_np = np.array([])
        self.val_loss_np = np.array([])
        self.train_acc = 0
        self.val_acc = 0

        # ------读取config2
        path = os.path.abspath('')
        with open(self.path + '/authentic/frontend/config2.yaml') as file:
            self.config = yaml.load(file, Loader=SafeLoader)
            self.credentials = self.config['credentials']
        self.credentials['usernames'] = {key.lower(): value for key, value in self.credentials['usernames'].items()}
        self.username = username
        self.cnn_project = self.credentials['usernames'][self.username]['project']['CNN']
        self.seg_project = self.credentials['usernames'][self.username]['project']['Segment']

        # ------读取config3
        with open(self.path + '/authentic/frontend/config3.yaml') as file:
            self.config3 = yaml.load(file, Loader=SafeLoader)
            self.project = self.config3['Project']
        self.project['name'] = {key.lower(): value for key, value in self.project['name'].items()}

    # 建立cookie
    @st.cache(allow_output_mutation=True)
    def get_manager(self):
        return stx.CookieManager('chart')
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

            # new一个工程
            st.write('───────新建工程────────')
            option1 = st.selectbox(
                'New a project',
                ('CNN', 'Segment'),
                key='slx1')
            name = st.text_input('输入名称')
            # ----------------------------新建工程------------------------------
            Sure = st.button('确定')
            if Sure:
                if option1 == 'CNN':
                    if len(name) > 0:
                        if name not in self.cnn_project:
                            # 添加信息进config2
                            self.config['credentials']['usernames'][self.username]['project'][
                                'CNN'] = self.cnn_project + list(name.split())
                            self.cnn_project = self.cnn_project + list(name.split())
                            with open(self.path+"/authentic/frontend/config2.yaml", "w", encoding="utf-8") as file:
                                yaml.dump(self.config, file)
                            # 添加信息进config3
                            self.config3['Project']['name'][name] = {'loss': 0, 'test_acc': 0, 'val_acc': 0}
                            with open(self.path+"/authentic/frontend/config3.yaml", "w", encoding="utf-8") as file:
                                yaml.dump(self.config3, file)
                        else:
                            st.error('文件名不能重复！')
                    else:
                        st.error('文件名不能为空！')
                elif option1 == 'Segment':
                    if len(name) > 0:
                        if name not in self.seg_project:
                            # 添加信息进config2
                            self.config['credentials']['usernames'][self.username]['project'][
                            'Segment'] = self.seg_project + list(name.split())
                            self.seg_project = self.seg_project + list(name.split())
                            with open(self.path+"/authentic/frontend/config2.yaml", "w", encoding="utf-8") as file:
                                yaml.dump(self.config, file)
                            # 添加信息进config3
                            self.config3['Project']['name'][name] = {'loss': 0, 'test_acc': 0, 'val_acc': 0}
                            with open(self.path+"/authentic/frontend/config3.yaml", "w",
                                      encoding="utf-8") as file:
                                yaml.dump(self.config3, file)
                        else:
                            st.error('文件名不能重复！')
                    else:
                        st.error('文件名不能为空！')
                # 向服务器发送新建dataset请求
                requests.post(self.url + f"/build/{name}")
                # self.config3['Project']['name'][name] = {'loss': 0, 'test_acc': 0, 'val_acc': 0}
                # with open("E:/ws/project1/authentic/frontend/config3.yaml", "w", encoding="utf-8") as file:
                #     yaml.dump(self.config3, file)
        # ----------------------------------主页面---------------------------------
        # 初始化信息
        val_acc = self.project['name'][st.session_state.pjtname]['val_acc']
        test_acc = self.project['name'][st.session_state.pjtname]['test_acc']

        st.write('──────────────────────────项目信息──────────────────────────')
        st.write('项目名称：', st.session_state.pjtname)
        st.write('所属人：', self.username)
        st.write('当前验证集精确度：', val_acc)
        st.write('当前测试集精确度：', test_acc)
    def preparing(self):
        send = 0
        with st.sidebar:
            st.write('───────数据处理────────')
            # 如果本地数据集为空，弹出警告
            # 增加上传button
            uploaded_imgs = st.file_uploader("上传数据集", accept_multiple_files=True)
            if st.button('上传'):
                send = 1
            # request
            multiple = st.text_input('输入增强倍数', '10')
            # ----------------数据增强开始-----------------
            cols1, cols2 = st.columns(2)
            cols1.button('begin')
            cols2.button('stop')
            # request
        # --------------------------------主页面----------------------------
        # request 查询本地有无data
        img_num = requests.post(self.url+f"/get_num/{st.session_state.pjtname}").json()
        # 向服务器上传数据集
        if send == 1:
            if len(uploaded_imgs) > 0:
                json_num = 0
                jpg_num = 0
                for i in range(len(uploaded_imgs)):
                    # 判断上传文件类型
                    if uploaded_imgs[i].name.split('.')[1] == 'json':
                        json_num += 1
                        result = requests.post(self.url+f"/upload_json/{st.session_state.pjtname}/{json_num+img_num}",
                                                files={'file': uploaded_imgs[i].getvalue()}).json()
                    elif uploaded_imgs[i].name.split('.')[1] == 'jpg':
                        jpg_num += 1
                        result = requests.post(self.url + f"/upload_jpg/{st.session_state.pjtname}/{jpg_num+img_num}",
                                               files={'file': uploaded_imgs[i].getvalue()}).json()
                    if result == 'error1':
                        st.error('图片上传失败!')
                        error = 1
                    elif result == 'error2':
                        st.error('json上传失败!')
                        error = 1
                    else:
                        error = 0
                if error != 1:
                    st.success('上传成功！')
                    # 因上传新数据导致数据集变化，再查询一次
                    img_num = requests.post(self.url+f"/get_num/{st.session_state.pjtname}").json()
            else:
                st.warning('请选择需要上传的图片！')
        # ------slide显示本地数据集
        if img_num == 0:
            st.warning('请上传数据集！')
        elif img_num == 1:
            img = requests.post(self.url + f"/{st.session_state.pjtname}/{1}").content
            st.image(img)
        elif img_num > 1:
            # imgs = [[]] * img_num
            # for i in range(img_num):
            #     imgs[i] = requests.post(self.url+f"/{st.session_state.pjtname}/{i+1}").content
            num = st.slider('查看标注后数据集', 1, img_num, 1)
            imgs = requests.post(self.url + f"/send/{st.session_state.pjtname}/{num}").content
            st.image(imgs)
        # 增强结束后显示处理后数据集
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
                    requests.post(self.url+f"/train_on")
                    self.trainon = 1
                    self.cookie_manager.set('train_on', 1)
                    st.session_state.trainon = 1
                    st.session_state.train_loss_list = []
                    st.session_state.val_loss_list = []
                else:
                    st.error('此工程不存在')
            if cols2.button('stop'):
                st.session_state.trainon = 0
                self.cookie_manager.set('train_on', 0, key='set2')
                # 设置cookie
                self.cookie_manager.set('loss', [st.session_state.train_loss_list, st.session_state.val_loss_list],
                                        expires_at=datetime.now() + timedelta(days=5))
        st.write('──────────────────────────loss曲线──────────────────────────')
        if st.button('clear'):
            self.cookie_manager.delete(cookie='loss')
            st.session_state.train_loss_list = 0
            st.session_state.val_loss_list = 0
        # st.write(self.cookie_manager.get_all())
        # st.write(self.cookie_manager.get("train_on"))
        # st.write(self.cookie_manager.get("loss"))
        cookies = self.cookie_manager.get_all()
        signal = self.cookie_manager.get("train_on")
        st.write(signal)
        if st.session_state.trainon == 0:
        # if self.cookie_manager.get("train_on") == 0:
            # st.write(self.cookie_manager.get('loss'))
            chart_data = pd.DataFrame(
                self.cookie_manager.get('loss'),
                index=['train loss', 'val loss']
            )
            chart = st.line_chart(chart_data.T)
            # st.write(cookies)
            st.write('train accuracy is: ', st.session_state.train_acc)
            st.write('validation accuracy is: ', st.session_state.val_acc)

        # ----------------------------主页面--------------------------
        # 绘制loss
        # 获取acc
        # 在config3中更改val_acc
        while True:
            if st.session_state.trainon == 1:
                loss = requests.post(self.url + f"/get_loss").json()
                self.train_acc = requests.post(self.url + f"/train").json()
                self.val_acc = requests.post(self.url + f"/val").json()
                self.draw(loss)
                self.config3['Project']['name'][st.session_state.pjtname]['val_acc'] = st.session_state.val_acc
                with open(self.path + "/authentic/frontend/config3.yaml", "w", encoding="utf-8") as file:
                    yaml.dump(self.config3, file)
            else:
                break



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
            project = 'a'
            num = 1
            bytes_data = requests.post(self.url+f"/{project}/{num}")
            st.image(bytes_data.content)
        '''
        实验
        向后端上传图片
        '''
    # 绘制loss，刷新acc
    def draw(self, loss):
        # loss = requests.post(self.url+f"/get_loss").json()
        train_loss = loss[0]
        val_loss = loss[1]
        self.train_loss_np = np.append(self.train_loss_np, train_loss)
        self.val_loss_np = np.append(self.val_loss_np, val_loss)
        st.session_state.train_loss_list.append(train_loss)
        st.session_state.val_loss_list.append(val_loss)
        chart_data = pd.DataFrame(
            np.array(list(zip(self.train_loss_np, self.val_loss_np))),
            columns=['train loss', 'val loss']
        )
        st.session_state.data = chart_data
        st.session_state.train_acc = self.train_acc
        st.session_state.val_acc = self.val_acc
        chart = st.empty()
        with chart.container():
            st.write("正在训练，请勿关闭界面...")
            st.line_chart(st.session_state.data)
            st.write('train accuracy is: ', st.session_state.train_acc)
            st.write('validation accuracy is: ', st.session_state.val_acc)
        time.sleep(2)
        chart.empty()
        # chart.line_chart(st.session_state.data)
        # st.session_state.trainon = 0

    def get_acc(self):
        train_acc = requests.post(self.url+f"/train").json()
        val_acc = requests.post(self.url+f"/val").json()

        # 训练完成后存储一次
        st.session_state.train_acc = self.train_acc
        st.session_state.val_acc = self.val_acc
        write_acc = st.empty()
        with write_acc.container():
            st.write('train accuracy is: ', st.session_state.train_acc)
            st.write('validation accuracy is: ', st.session_state.val_acc)
        time.sleep(0.5)
        write_acc.empty()
    def setup(self):
        self.navigation_bar()





