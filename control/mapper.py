
def map_screen_to_kmbox(x,y,sw=1920,sh=1080):
    return int(x/sw*255), int(y/sh*255)
