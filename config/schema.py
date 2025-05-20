
from pydantic import BaseModel, Field

class Config(BaseModel):
    kmbox_mode: str = Field("net", pattern="^(net|serial)$")
    host: str | None = None
    port: int | None = None
    serial_port: str | None = None
    baud: int | None = None
    model_path: str
    device: str | None = "cpu"
