from api.user.entity.user import User
from api.user.repository.user_repository import UserRepository


class UserService:
    """
    Service class to handle business logics related to users

    Args:
        user_repository (UserRepository): user repository instance
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, **kwargs) -> User:
        """
        Register a new user in the database.

        Args:
            **kwargs: parameters for creating user instance

        Returns:
            User: registered user

        Todo:
            - validate user kwargs
        """
        new_user = User(**kwargs)
        saved_user = await self.user_repository.save(new_user)

        return saved_user

    async def find_user_by_id(self, user_id: int) -> User:
        """"""
        return await self.user_repository.find_user_by_id(user_id)

    async def delete(self, user_id: int):
        """
        Update the user's deleted_at to the current time.

        Args:
            user_id (int): The ID of the user to delete

        Notes:
            Through the batch task at 00:00 every day,
            users who have passed 30 days from deleted_at are deleted.
        """
        await self.user_repository.update_deleted_at(user_id)

    async def is_registered_user(self, email: str) -> bool:
        """
        Check to see if there is already user with specific email.

        Args:
            email (str): Email for duplicate verification

        Returns:
            bool: Is the user already registered.
        """
        user = await self.user_repository.find_user_by_email(email)

        return user is not None
