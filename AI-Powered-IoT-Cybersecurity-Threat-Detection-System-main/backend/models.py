from typing import Optional
from pydantic import BaseModel


class DeviceData(BaseModel):
    device_id: str
    temperature: float
    humidity: Optional[float] = None
    cpu_usage: float
    packet_rate: int
    failed_login: int
    wifi_signal: int
    heap: Optional[float] = None
    uptime: Optional[float] = None