from server.applications.application_library import ApplicationLibrary
from server.applications.light_application_manager import LightApplicationManager
from server.device.registry import DeviceRegistry
from server.device.room_registry import RoomRegistry

from flask import Blueprint, request

def build_application_route(
    lib: ApplicationLibrary,
    manager: LightApplicationManager,
    rooms: RoomRegistry,
    lights: DeviceRegistry):

    application_blueprint = Blueprint("application", __name__)

    @application_blueprint.route("/", methods=["GET"])
    def list_applications():
        return {
            "applications": list(lib.applications.keys())
        }

    @application_blueprint.route("/<application_name>/start", methods=["POST"])
    def start_application(application_name: str):
        body = request.json
        grid_type = body['grid_type']
        room_or_light_id = body['grid_id']
        if grid_type == "room":
            room_wrapper = rooms.get_room(room_or_light_id)
            grid = room_wrapper.grid
            application = manager.start_application(application_name, grid)
        else:
            light_wrapper = lights.get_light_device(None, name=room_or_light_id)
            grid = light_wrapper.grid_object
            application = manager.start_application(application_name, grid)
        
        return {
            "application_class": application_name,
            "instance_id": id(application)
        }
    
    @application_blueprint.route("/<application_id>/stop", methods=["POST"])
    def stop_application(application_id: str):
        application_id = int(application_id)
        manager.kill_application(application_id)
        return {
            "running_applications": list(manager._running_applications.keys())
        }

    return application_blueprint