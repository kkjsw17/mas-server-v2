from sqlalchemy import delete, select, update

from api.database.database_connection_manager import DatabaseConnectionManager
from api.user.entity.user import User
from api.user.exception.user_exception import UserNotFoundException
from api.utils.datetime_utils import get_now_datetime_by_timezone


class UserRepository:
    """
    Repository class for managing User objects in the database.

    Args:
        database (DatabaseConnectionManager): database connection management classㄹ
    """

    def __init__(self, database: DatabaseConnectionManager):
        self.database = database

    async def find_user_by_id(self, user_id: int) -> User:
        """
        Find a user with the given user ID.

        Args:
            user_id (int): The ID of the user to find.

        Returns:
            User: Found User.

        Exceptions:
            UserNotFoundException: If no user with the given ID is found in the database.
        """
        async with self.database.get_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))

            user = result.scalars().one_or_none()
            if user is None:
                raise UserNotFoundException

        return user

    async def find_user_by_email(self, email: str) -> User | None:
        """
        Find a user with the given email.

        Args:
            email (int): The email address of the user to find.

        Returns:
            User | None: Found User or None.
        """
        async with self.database.get_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().one_or_none()

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

    async def update_deleted_at(self, user_id: int):
        """
        Update a deleted_at column of a user with the given ID from the database.

        Args:
            user_id (int): The ID of the user to update deleted_at.

        Notes:
            Through the batch task at 00:00 every day,
            users who have passed 30 days from deleted_at are deleted.
        """
        async with self.database.get_session() as session:
            now_datetime = get_now_datetime_by_timezone()
            await session.execute(
                update(User).where(User.id == user_id).values(deleted_at=now_datetime)
            )

    async def delete(self, user_id: int) -> User | None:
        """
        Delete a user with the given user ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            User | None: Deleted user or None
        """
        async with self.database.get_session() as session:
            result = await session.execute(delete(User).where(User.id == user_id))

            deleted_user = result.scalars().one_or_none()

        return deleted_user
