
from fastapi import FastAPI, UploadFile
import socketio, cv2, numpy as np, time

from ai_engine.detector import Detector
from ai_engine.tracker import ByteTracker
from control.mapper import map_screen_to_kmbox
from control.kmbox_protocol.net_adapter.net_client import NetKMBox

det=Detector(); trk=ByteTracker()
kmbox=NetKMBox()

sio=socketio.AsyncServer(async_mode='asgi',cors_allowed_origins='*')
app=FastAPI()
app.mount("/ws",socketio.ASGIApp(sio,socketio_path=''))

@app.post("/detect")
async def detect(file:UploadFile):
    t0=time.time()
    data=await file.read()
    img=cv2.imdecode(np.frombuffer(data,np.uint8),cv2.IMREAD_COLOR)
    boxes=det.predict(img)
    tracks=trk.update(boxes)
    if tracks:
        box=tracks[0]['box']
        x=(box[0]+box[2])//2; y=(box[1]+box[3])//2
        kx,ky=map_screen_to_kmbox(x,y)
        kmbox.send(kx,ky)
    latency_ms=int((time.time()-t0)*1000)
    await sio.emit('hud',{'fps':1,'latency':latency_ms,'tracks':tracks})
    return {'latency_ms':latency_ms,'tracks':tracks}
