import io
import json
import os
import numpy as np
import pandas as pd
import numpy as np
import requests
from PIL import Image
from pandas.core.frame import DataFrame

# a = 'a'
# bytes_data = requests.post(f"http://127.0.0.1:8000/{a}").json()
# print(bytes_data)

# data = requests.get(f"http://127.0.0.1:8080/pic")
# image = Image.open(io.BytesIO(data.content))

# PATH = 'E:/dataset/a'
# pics = os.listdir(PATH)
# for pic in pics:
#     print(PATH+'/'+pic)
# PATH = 'E:/dataset/'+'a'
# pics = os.listdir(PATH)
# for i in range(len(pics)):
#     pics[i] = 'E:/dataset/'+'a' + pics[i]
#
# print(pics)
os.mkdir('E:/dataset/b')
