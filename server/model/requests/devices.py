import pydantic

class CreateDeviceFromPartialPOST(pydantic.BaseModel):
    name: str
    grid: str