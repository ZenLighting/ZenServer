from server.model.sqlite_models import LightDeviceModel, LightDeviceWrapper
from server.model.grid import LightGrid, GridSpace, PixelGridSpace

light = LightDeviceModel(
    id=0,
    name="test_light",
    grid_string= "x----\n-x---\n--x--\n---x-\n----x\n",
    last_address="192.168.1.2"
)

funct_light = LightDeviceWrapper(light)

print(funct_light.grid_object)

light_room = LightGrid("------\n------\n------\n------\n------\n------\n")

print()
print(light_room)
light_room.transpose_grid(funct_light.grid_object, (2,2), expand=True)

print(light_room)