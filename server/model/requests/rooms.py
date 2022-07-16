import pydantic

class AddLightToRoomPOST(pydantic.BaseModel):
    light: str
    x: int
    y: int

class SetRoomColorPOST(pydantic.BaseModel):
    r: int
    g: int
    b: int