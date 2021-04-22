import pydantic

class LightUpdate(pydantic.BaseModel):
    index: int
    r: int
    g: int
    b: int