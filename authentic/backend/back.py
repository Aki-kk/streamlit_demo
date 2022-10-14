import os
import glob
import zipfile
import io

from PIL import Image
from fastapi import FastAPI, Response, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
import uvicorn
import random

from fastapi.responses import FileResponse

app = FastAPI()

epoch = 0
loss = [0, 0]
stop = 0


# begin train
@app.post("/train_on")
def train():
    global trainon
    trainon = 1

# 获取train_acc
@app.post("/train")
def train():
    return JSONResponse(content=0.99,
                        status_code=202,
                        headers={'a':'b'})
# 获取val_acc
@app.post("/val")
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
    path = 'E:/dataset/'+project
    os.mkdir(path)
# 向服务器上传图片并保存
# @app.post("/uploads")
# async def upload_files(files: List[UploadFile] = File(...)):
#     return await save_files(files)

@app.post("/upload/{project}/{id}")
async def upload(project: str, id: int, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        PATH = 'E:/dataset/'+project+'/'+str(id)+'.jpg'
        with open(PATH, 'wb') as f:
            f.write(contents)
    except Exception:
        return 'error'
    finally:
        await file.close()

    return 'success'

# 将该工程下的数据集依次传输回前端
@app.post('/{project}/{num}')
def get_pic(project: str, num: int):
    PATH = 'E:/dataset/' + project
    image_path = PATH + '/' + str(num) + '.jpg'
    return FileResponse(image_path)

# 获取服务器下该工程的数据集数量
@app.post("/{project}")
def get_pjt(project: str):
    PATH = 'E:/dataset/'+project
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
    uvicorn.run(app='back:app', host="10.110.77.190", port=8000, reload=True, debug=True)

