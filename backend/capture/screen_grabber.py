"""Screen capture abstraction layer.

TODO: Implement platform‑specific grabbers (Win32, X11, Wayland, etc.).
For now, this scaffold returns a black frame to unblock downstream logic.
"""

from typing import Tuple
import numpy as np

class ScreenGrabber:
    """High‑level API for obtaining RGB frames from the primary display."""

    def __init__(self, monitor: int | None = None) -> None:
        self.monitor = monitor or 0  # default primary

    def grab(self) -> Tuple[np.ndarray, float]:
        """Capture a frame.

        Returns
        -------
        frame : np.ndarray
            Dummy black image (1080p) until real implementation provided.
        ts : float
            Unix timestamp when the frame was captured.
        """
        import time
        frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        return frame, time.time()
