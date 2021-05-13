from typing import Any, List, Tuple
import pydantic

class DeviceRegistrationMessage(pydantic.BaseModel):
    type: str
    dId: str
    data: Any

class LightDeviceRegistrationData(pydantic.BaseModel):
    state: List[Tuple[str, str, str]]

class LightDeviceRegistrationMessage(DeviceRegistrationMessage):
    data: LightDeviceRegistrationData