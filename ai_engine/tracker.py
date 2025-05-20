
import numpy as np

def iou(b1, b2):
    x1 = max(b1[0], b2[0]); y1 = max(b1[1], b2[1])
    x2 = min(b1[2], b2[2]); y2 = min(b1[3], b2[3])
    inter = max(0,x2-x1)*max(0,y2-y1)
    area1=(b1[2]-b1[0])*(b1[3]-b1[1])
    area2=(b2[2]-b2[0])*(b2[3]-b2[1])
    union = area1+area2-inter
    return inter/union if union>0 else 0

class Track:
    def __init__(self, box, tid):
        self.box=box; self.id=tid; self.hits=1; self.missed=0

class ByteTracker:
    def __init__(self, iou_thres=0.3, max_missed=30):
        self.iou_thres=iou_thres
        self.max_missed=max_missed
        self.tracks=[]
        self._next_id=0
    def update(self, detections):
        updated=[]
        for trk in self.tracks:
            trk.missed+=1
        for det in detections:
            best_t=None; best=0
            for trk in self.tracks:
                i=iou(det,trk.box)
                if i>best and i>=self.iou_thres:
                    best=i; best_t=trk
            if best_t:
                best_t.box=det; best_t.hits+=1; best_t.missed=0
                updated.append(best_t)
            else:
                t=Track(det,self._next_id); self._next_id+=1
                self.tracks.append(t); updated.append(t)
        self.tracks=[t for t in self.tracks if t.missed<=self.max_missed]
        return [{'id':t.id,'box':t.box} for t in updated]
