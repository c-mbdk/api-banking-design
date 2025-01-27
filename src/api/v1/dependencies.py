from src.db.database import DatabaseClient
from src.logger import logger


async def get_database_client() -> DatabaseClient:
    """
    Initialises database client to be reused throughout the application.
    """
    global _DATABASE_CLIENT

    if _DATABASE_CLIENT is None:
        _DATABASE_CLIENT = DatabaseClient()
        await _DATABASE_CLIENT.initialise()
        logger.debug("Created and initialised new DatabaseClient.")

    return _DATABASE_CLIENT
