from server.rooms.room import Room

class RoomRegistry(object):

    def __init__(self):
        self.rooms_by_id = {}

    def create_empty_room(self, name):
        if self.rooms_by_id.get(name) is None:
            new_room = Room(name)
            self.rooms_by_id[name] = new_room

    def get_room(self, name):
        return self.rooms_by_id.get(name)

    def list_all_rooms(self):
        return list(self.rooms_by_id.keys())