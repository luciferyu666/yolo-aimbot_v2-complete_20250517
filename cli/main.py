
import argparse, yaml, cv2
from ai_engine.detector import Detector
from ai_engine.tracker import SimpleTracker
from ai_engine.postprocess import select_center
from control.mapper import map_screen_to_kmbox
from control.kmbox_protocol.net_adapter.net_client import NetKMBox
from control.kmbox_protocol.serial_adapter.serial_client import SerialKMBox

def parse():
    ap=argparse.ArgumentParser()
    ap.add_argument('--config',required=True)
    ap.add_argument('--source',required=True)
    return ap.parse_args()

def main():
    args=parse()
    cfg=yaml.safe_load(open(args.config))
    det=Detector(cfg['model_path'])
    trk=SimpleTracker()
    img=cv2.imread(args.source)
    boxes=det.predict(img)
    tracked=trk.update(boxes)
    best=select_center(tracked)
    if not best:
        print("No detection");return
    x_mid=(best[0]+best[2])//2
    y_mid=(best[1]+best[3])//2
    kx,ky = map_screen_to_kmbox(x_mid,y_mid)
    if cfg['kmbox_mode']=='serial':
        cli=SerialKMBox(cfg['serial_port'],cfg['baud'])
    else:
        cli=NetKMBox(cfg['host'],cfg['port'])
    cli.send(kx,ky)
    print("Sent to KMBox",kx,ky)

if __name__=="__main__":
    main()
