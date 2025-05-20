
import collections, statistics
class LatencyComp:
    def __init__(self, window=60, base=0.05):
        self.buf=collections.deque(maxlen=window); self.base=base
    def record(self,dur): self.buf.append(dur)
    def delay(self):
        return max(self.base - (statistics.mean(self.buf) if self.buf else 0), 0)
