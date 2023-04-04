from sqlalchemy import select, update

from mas.database.database_connection_manager import DatabaseConnectionManager
from mas.user.entity.user import User
from mas.user.exception.user_exception import UserNotFoundException
from mas.utils.datetime_utils import get_now_datetime_by_timezone


class UserRepository:
    """
    Repository class for managing User objects in the database.

    Args:
        database (DatabaseConnectionManager): database connection management class
    """

    def __init__(self, database: DatabaseConnectionManager):
        self.database = database

    async def find_user_by_id(self, user_id: int) -> User:
        """
        Find a user with the given user ID.

        Args:
            user_id (int): The ID of the user to find.

        Returns:
            User: The User object representing the found user.

        Exceptions:
            UserNotFoundException: If no user with the given ID is found in the database.
        """
        async with self.database.get_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))

            user = result.scalars().one_or_none()
            if user is None:
                raise UserNotFoundException

        return user

    async def save(self, user: User) -> User:
        """
        Save the given user object to the database.

        Args:
            user (User): The User object to save to the database.

        Returns:
            User: The saved User object.
        """
        async with self.database.get_session() as session:
            session.add(user)

        return user

    async def delete(self, user_id: int):
        """
        Update a deleted_at column of a user with the given ID from the database.

        Args:
            user_id (int): The ID of the user to delete.

        Notes:
            Through the batch task at 00:00 every day,
            users who have passed 30 days from deleted_at are deleted.
        """
        async with self.database.get_session() as session:
            now_datetime = get_now_datetime_by_timezone()
            await session.execute(
                update(User).where(User.id == user_id).values(deleted_at=now_datetime)
            )
