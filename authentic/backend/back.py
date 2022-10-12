import io
from PIL import Image
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import random

from starlette.responses import FileResponse

app = FastAPI()

epoch = 0
loss = [0, 0]
stop = 0

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 前端向后端传递参数
@app.post("/{lr}")
def get_loss(lr: str):
    return lr
# begin train
@app.get("/train_on")
def train():
    global trainon
    trainon = 1

# 获取train_acc
@app.get("/train")
def train():
    return JSONResponse(content=0.99,
                        status_code=202,
                        headers={'a':'b'})
# 获取val_acc
@app.get("/val")
def val():
    return JSONResponse(content=0.98,
                        status_code=202,
                        headers={'a':'b'})
# 刷新数据，前端向后端询问
@app.post("/ask")
def get_loss():
    if stop != 1:
        if(epoch%5 == 0):
            return loss
        else:
            return -1
    else:
        return 0
trainon = 0
@app.get("/ask1")
def get_loss():
    if trainon != 0:
        loss = [random.random(), random.random()]
        return JSONResponse(content=loss,
                            status_code=202,
                            headers={'a': 'b'})
    else:
        return JSONResponse(content=0,
                            status_code=202,
                            headers={'a': 'b'})
@app.get('/pic')
def get_pic():
    image_path = 'E:/dataset/001_test/1.jpeg'
    image = Image.open(image_path)
    byte_data = image2byte(image)

    return FileResponse(image_path)

def image2byte(image):
    '''
    图片转byte
    image: 必须是PIL格式
    image_bytes: 二进制
    '''
    # 创建一个字节流管道
    img_bytes = io.BytesIO()
    # 将图片数据存入字节流管道， format可以按照具体文件的格式填写
    image.save(img_bytes, format="JPEG")
    # 从字节流管道中获取二进制
    image_bytes = img_bytes.getvalue()
    return image_bytes

def byte2image(byte_data):
    '''
    byte转为图片
    byte_data: 二进制
    '''
    image = Image.open(io.BytesIO(byte_data))
    return image

if __name__ == '__main__':
    uvicorn.run(app='back:app', host="127.0.0.1", port=8000, reload=True, debug=True)

