import os
import dotenv
dotenv.load_dotenv()


MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
DB_URI = os.getenv("DATABASE_URI", "")