from server.model.sqlite_models import LightDeviceModel
from server.model.light import LightDeviceWrapper
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

# this works, check hash values to determin correct placement
light_grid = LightGrid("000 000 000 003 002 001 000 000 000")
print(light_grid)
for row in light_grid.grid_object:
    for light in row:
        print(hash(light), end=" ")
    print("")
for light in light_grid.pixels_by_index:
    print(hash(light), end=" ")