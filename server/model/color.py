from dataclasses import dataclass

@dataclass
class ColorProfile(object):
    name: str
    r: int
    g: int
    b: int