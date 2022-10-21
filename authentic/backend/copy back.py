import os
import glob
import zipfile
import io

import cv2
from PIL import Image
from fastapi import FastAPI, Response, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
import uvicorn
import random
from utility import __draw_lable
from fastapi.responses import FileResponse

app = FastAPI()

epoch = 0
loss = [0, 0]
stop = 0

# begin augment
@app.get("/aug_on")
def train():
    return 'success'
# begin train
@app.get("/train_on")
def train_begin():
    return 'success'

# stop train
@app.get("/train_stop")
def train_stop():
    return 'success'
# 获取train_acc
@app.post("/train")
def train_loss():
    return JSONResponse(content=0.99,
                        status_code=202,
                        headers={'a':'b'})
# 获取val_acc
@app.post("/val")
def val_loss():
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
@app.post("/ask1")
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
# 向服务器发送新建dataset请求
@app.post("/build/{project}")
def build_dataset(project: str):
    path = 'E:/dataset/' + project + '/src'
    os.makedirs(path)
    path = 'E:/dataset/' + project + '/lable'
    os.makedirs(path)
# 向服务器上传图片并保存
# jpg格式
@app.post("/upload_jpg/{project}/{id}")
async def upload(project: str, id: int, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image_path = 'E:/dataset/' + project + '/src/' + str(id) + '.jpg'
        json_path = 'E:/dataset/' + project + '/src/' + str(id) + '.json'
        with open(image_path, 'wb') as f:
            f.write(contents)
        try:
            img = __draw_lable(image_path, json_path, (0, 222, 120))
            PATH = 'E:/dataset/' + project + '/lable/' + str(id) + '.jpg'
            cv2.imwrite(PATH, img)
        except:
            return 'None'
    except Exception:
        return 'error1'
    finally:
        await file.close()
    return 'success'
# json格式
@app.post("/upload_json/{project}/{id}")
async def upload(project: str, id: int, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image_path = 'E:/dataset/'+project+'/src/'+str(id)+'.jpg'
        json_path = 'E:/dataset/'+project+'/src/'+str(id)+'.json'
        with open(json_path, 'wb') as f:
            f.write(contents)
        try:
            img = __draw_lable(image_path, json_path, (0, 222, 120))
            PATH = 'E:/dataset/'+project+'/lable/'+str(id)+'.jpg'
            cv2.imwrite(PATH, img)
        except:
            return 'None'
    except Exception:
        return 'error1'
    finally:
        await file.close()
    return 'success'

# 将该工程下的数据集依次传输回前端
@app.post('/{project}/{num}')
def get_pic(project: str, num: int):
    PATH = 'E:/dataset/' + project + '/lable'
    image_path = PATH + '/' + str(num) + '.jpg'
    return FileResponse(image_path)

# 获取服务器下该工程的数据集数量
@app.post("/{project}")
def get_pjt(project: str):
    PATH = 'E:/dataset/'+project+'/lable'
    pics = os.listdir(PATH)
    return JSONResponse(content=len(pics),
                        status_code=202,
                        headers={'a': 'b'})

async def save_files(files):
    for file in files:
        "type:<class 'coroutine'>"
        cont = await file.read()
        with open(f'myfiles/{file.filename}.jpg', 'wb') as f:
            f.write(cont)
    return 'success'

def zipfiles(filenames):
    zip_subdir = "archive"
    zip_filename = "%s.zip" % zip_subdir
    # Open StringIO to grab in-memory ZIP contents
    s = io.BytesIO()
    # The zip compressor
    zf = zipfile.ZipFile(s, "w")
    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        # Add file, at correct path
        zf.write(fpath, zip_path)
    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(s.getvalue(), media_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp


if __name__ == '__main__':
    uvicorn.run(app='back:app', host="0.0.0.0", port=8000, reload=True, debug=True)

