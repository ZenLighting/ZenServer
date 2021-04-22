from server.finders.light_tracker import LightTracker
from flask import Blueprint, request
import json
from server.controllers.database import SessionWrapper
from server.model.sqlmodel import Light

def create_light_bp(light_tracker: LightTracker):

    light_blueprint = Blueprint("light", __name__)

    @light_blueprint.route("/")
    def list_lights():
        return {
            "status": 200,
            "data": list(light_tracker.light_information_map.values())
        }

    @light_blueprint.route("/unregistered")
    def list_unreg_lights():
        return_list = []
        for light_uuid in light_tracker.lights_not_in_database:
            return_list.append(light_tracker.light_information_map[light_uuid])

        return {
            "status": 200,
            "data": return_list
        }

    @light_blueprint.route("/registered")
    def light_reg_lights():
        return_list = []
        for light_uuid in light_tracker.uuids_in_database:
            return_list.append(light_tracker.light_information_map[light_uuid])
        return {
            "status": 200,
            "data": return_list
        }

    @light_blueprint.route("/<uuid>/register")
    def register_light_to_room(uuid):
        light_tracker.register_untracked_light(uuid)
        return_list = []
        for light_uuid in light_tracker.uuids_in_database:
            return_list.append(light_tracker.light_information_map[light_uuid])
        return {
            "status": 200,
            "data": return_list
        }

    @light_blueprint.route("/<uuid>/set_layout", methods=["POST"])
    def register_new_light_layout(uuid):
        body = request.json
        text_encoded_layout = body['text_encoded_layout']
        # get light object
        light_obj: Light = light_tracker.light_information_map[uuid]
        # create session
        with SessionWrapper() as session:
            session.add(light_obj)
            light_obj.light_space = text_encoded_layout
            session.commit()
            light_obj_res = light_obj.to_dict()
        
        return {
            "status": 200,
            "data": light_obj_res
        }

    return light_blueprint