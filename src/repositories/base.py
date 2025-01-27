from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar
import uuid

from sqlmodel import Session

from src.db.database import DatabaseClient


# T (from Python 3.12 is throwing errors)
# Base class here used to define a generic class
class Base:
    pass

ModelType = TypeVar('ModelType', bound=Base)

class AbstractRepository[T](ABC):  # noqa: E999
    """
    Base repository class to be used for all repositories which require all methods.
    """

    def __init__(self, db: DatabaseClient):
        """
        Initialises the repository with a database connection pool.

        Args:
            db (DatabaseClient): An instance of the db connection pool.
        """
        self._db = db


    @abstractmethod
    def get_by_guid(self, guid: uuid.UUID) -> ModelType:
        """
        Retrieves data for a given object from the database.
        The exact object is specified upon implementation.

        Args:
            guid (uuid.UUID): ID for the given object.

        Returns:
            T: The domain object.
        """
        raise NotImplementedError
    

    def get_all(self) -> List[ModelType]:
        """
        Retrieves data from the database as domain objects.
        The exact object type is specified upon implementation.

        Returns:
            List[T]: A list of domain objects
        """
        raise NotImplementedError
    
    @abstractmethod
    def update(self, guid: uuid.UUID, **kwargs: object) -> None:
        """
        Updates the domain object's details (in the database).
        This method is overridden upon implementation.

        Args:
            guid (uuid.UUID): The ID of the domain object
            kwargs (object): The properties to be updated on the object
        """
        raise NotImplementedError
    

    @abstractmethod
    def delete(self, guid: uuid.UUID) -> None:
        """
        Deletes a domain object's record(s) from the database.

        Args:
            guid (uuid.UUID): The ID of the object.
        """
        raise NotImplementedError
    

class AbstractAllRepository(AbstractRepository):
    """
    Additional base repository class that extends the original: create method supported.
    """

    @abstractmethod
    def create(self, **kwargs: object) -> None:
        """
        Creates a domain object's record(s) in the database.

        Args:
            kwargs (object): The properties of the object.
        """
        raise NotImplementedError


# class AbstractRUDRepository(Generic[ModelType](ABC)):
#     """
#     Base repository class: supports all methods except creation.
#     """

#     def __init__(self, session: Session):
#         """
#         Initialises the repository with a database session.

#         Args:
#             session (Session): The database session.
#         """
#         self.session = session

