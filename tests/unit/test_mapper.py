
from control.mapper import map_screen_to_kmbox
def test_map():
    kx,ky = map_screen_to_kmbox(960,540)
    assert 120<=kx<=136 and 120<=ky<=136
