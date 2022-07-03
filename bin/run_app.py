from email.policy import default
from server.app import ZenServerApp, ZenServerConfig
import optparse
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session
from server.model.sqlite_models import Base
import os

parser = optparse.OptionParser()
parser.add_option("-d", "--create-db", action="store_true", dest="create_database", help="flag to determin whether to create database in sqlite file")
parser.add_option("-c", "--config", action="store", dest="config_path", help="the path to the config json file")
(options, args) = parser.parse_args()
print(options, args)

if options.config_path:
    config = ZenServerConfig.parse_file(options.config_path)
else:
    config = ZenServerConfig(port=8080)

#print(os.listdir("/config"))

if options.create_database:
    engine = create_engine(config.sqlite_uri)
    Base.metadata.create_all(engine)
    print(engine.table_names())
"""    with Session(bind=engine).begin() as session:
        session: Session
        print(session.)"""

app = ZenServerApp(config)
app.start()