
from ai_engine.tracker import ByteTracker
def test_track():
    trk=ByteTracker()
    det=[(0,0,10,10,0.9)]
    t=trk.update(det)
    assert t[0]['id']==0
