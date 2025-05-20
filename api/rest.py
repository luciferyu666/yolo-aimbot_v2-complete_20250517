
from fastapi import FastAPI, UploadFile
import cv2, numpy as np, asyncio
import socketio

from ai_engine.detector import Detector
from ai_engine.tracker import SimpleTracker
from ai_engine.postprocess import select_center
from control.mapper import map_screen_to_kmbox
from control.kmbox_protocol.net_adapter.net_client import NetKMBox

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
app.mount("/ws", socketio.ASGIApp(sio, socketio_path=''))

det = Detector('ai_engine/models/yolov8n.onnx')
trk = SimpleTracker()
kmbox = NetKMBox()

@app.post("/detect")
async def detect(file: UploadFile):
    data=await file.read()
    img=cv2.imdecode(np.frombuffer(data,np.uint8),cv2.IMREAD_COLOR)
    boxes=det.predict(img)
    tracked=trk.update(boxes)
    best=select_center(tracked)
    if best:
        x_mid=(best[0]+best[2])//2
        y_mid=(best[1]+best[3])//2
        kx,ky = map_screen_to_kmbox(x_mid,y_mid)
        kmbox.send(kx,ky)
    await sio.emit('det', {'boxes':boxes})
    return {'boxes':boxes}

@app.get("/")
async def root():
    return {"msg":"OK"}
