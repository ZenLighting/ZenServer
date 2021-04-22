from server.model.sqlmodel import Light
from server.controllers.database import SessionWrapper
from typing import List

class LightTracker(object):

    def __init__(self):
        self.uuids_in_database = set()
        self.lights_not_in_database = set()
        self.light_information_map = dict() # uuid to database object
        self.populate_from_database()
    
    def populate_from_database(self):
        with SessionWrapper() as session:
            lights: List[Light] = session.query(Light).all()
            for light in lights:
                self.uuids_in_database.add(light.uuid)
                self.light_information_map[light.uuid] = light

    def add_available_light(self, new_light: Light):
        if new_light.uuid not in self.uuids_in_database:
            self.lights_not_in_database.add(new_light.uuid)
            self.light_information_map[new_light.uuid] = new_light

    def register_untracked_light(self, uuid: str):
        with SessionWrapper() as session:
            light_obj = self.light_information_map.get(uuid)
            session.add(light_obj)
            session.commit()
            self.populate_from_database()
            self.lights_not_in_database.clear()
        
    
