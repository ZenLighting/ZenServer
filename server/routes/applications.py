from server.applications.application_library import ApplicationLibrary
from server.applications.light_application_manager import LightApplicationManager
from server.device.registry import DeviceRegistry
from server.device.room_registry import RoomRegistry

from flask import Blueprint, request

from server.model.requests.application import StartApplicationRequest

def build_application_route(
    lib: ApplicationLibrary,
    manager: LightApplicationManager,
    rooms: RoomRegistry,
    lights: DeviceRegistry):

    application_blueprint = Blueprint("device", __name__)

    @application_blueprint.route("/", methods=["GET"])
    def list_applications():
        return {
            "applications": list(lib.applications.keys())
        }

    @application_blueprint.route("/<app_id>/details")
    def get_application_details(app_id):
        application = lib.applications.get(int(app_id))
        try:
            app_repr = application.json()
        except Exception as err:
            app_repr = {
                "message": "cant get representation of the application"
            }
        
        return {
            app_id: app_repr
        }

    @application_blueprint.route("/<application_name>/start", methods=["POST"])
    def start_application(application_name: str):
        body = StartApplicationRequest.parse_obj(request.json)
        grid_type = body.grid_type
        room_or_light_id = body.grid_id
        if grid_type == "room":
            room_wrapper = rooms.get_room(room_or_light_id)
            grid = room_wrapper.grid
            application = manager.start_application(application_name, body.application_args, grid, body.schedule)
        else:
            light_wrapper = lights.get_light_device(None, name=room_or_light_id)
            grid = light_wrapper.grid_object
            application = manager.start_application(application_name, body.application_args, grid, body.schedule)
        
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