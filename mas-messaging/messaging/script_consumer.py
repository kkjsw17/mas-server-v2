import asyncio
import os

from messaging.database.mysql_connection_manager import MySQLConnectionManager
from messaging.repository.script_repository import ScriptRepository
from messaging.service.script_consuming_service import ScriptConsumingService
from messaging.utils.config import Config

config = Config(os.getenv("PHASE", "local"))
database_connection = MySQLConnectionManager(config=config)
asyncio.run(database_connection.connect_db())
script_repository = ScriptRepository(database=database_connection)
script_consuming_service = ScriptConsumingService(config, script_repository)

if __name__ == "__main__":
    asyncio.run(script_consuming_service.consume_script())
