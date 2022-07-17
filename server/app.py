import pydantic
from server.device.registry import DeviceRegistry
from server.device.room_registry import RoomRegistry
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from flask_cors import CORS
from flask import Flask
import server.routes.device as deviceRoute 
import server.routes.rooms as RoomRoute
from server.finders.deviceHeartbeat import DeviceHeartbeatDetector
from threading import Thread

class ZenServerConfig(pydantic.BaseModel):
    host: str = "0.0.0.0"
    port: int = 80
    sqlite_uri :str = "sqlite:////home/gfvandehei/.zenserver/data.db"

class ZenServerApp(object):

    def __init__(self, config: ZenServerConfig):
        self.config = config
        self.engine = create_engine(config.sqlite_uri)
        self.session_maker = sessionmaker(self.engine)
        
        self.registry = DeviceRegistry(self.session_maker)
        self.room_registry = RoomRegistry(self.session_maker, self.registry)
        self.light_heartbeat_sensor = DeviceHeartbeatDetector(self.registry)
        self.light_detection_thread = Thread(target=self.light_heartbeat_sensor.run)
        self.light_detection_thread.start()

        self.app = Flask(__name__, static_folder="./static", static_url_path="/static")
        CORS(self.app)

        self.app.register_blueprint(deviceRoute.create_blueprint(self.registry, self.session_maker), url_prefix="/device")
        self.app.register_blueprint(RoomRoute.create_blueprint(self.room_registry, self.registry), url_prefix="/room")
    
    def start(self):
        self.app.run(host=self.config.host, port=self.config.port)
        #pass

