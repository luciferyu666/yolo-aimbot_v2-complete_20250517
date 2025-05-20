
def select_center(tracked):
    if not tracked: return None
    # choose first track
    return tracked[0]['box']
