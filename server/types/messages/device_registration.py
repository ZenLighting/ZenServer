from typing import Any, List, Optional, Tuple
import pydantic

class DeviceRegistrationMessage(pydantic.BaseModel):
    type: str
    dId: str
    data: Any
    last_detected: Optional[float]

class LightDeviceRegistrationData(pydantic.BaseModel):
    state: List[Tuple[str, str, str]]

class LightDeviceRegistrationMessage(DeviceRegistrationMessage):
    data: LightDeviceRegistrationData