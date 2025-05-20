
from control.latency import LatencyComp
def test_delay():
    l=LatencyComp()
    l.record(0.01); l.record(0.02)
    assert l.delay()>=0
