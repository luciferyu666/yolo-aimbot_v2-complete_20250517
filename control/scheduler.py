
import time, threading
class Scheduler:
    def __init__(self, client, latency):
        self.client=client; self.latency=latency; self._run=False
    def start(self,x,y):
        if self._run: return
        self._run=True
        threading.Thread(target=self._loop,args=(x,y),daemon=True).start()
    def _loop(self,x,y):
        while self._run:
            t0=time.time()
            self.client.send(x,y)
            self.latency.record(time.time()-t0)
            time.sleep(self.latency.delay())
    def stop(self): self._run=False
