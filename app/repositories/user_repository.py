

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, db

class UserRepository:
    def __init__(self):
        self.session = db.session

    def get_user(self, user_id):
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The user object if found, otherwise None.
        """
        try:
            return self.session.query(User).filter_by(user_id=user_id).first()
        except Exception as e:
            self.session.rollback()
            raise e

    def create_user(self, user_data):
        """
        Creates a new user.

        Args:
            user_data (dict): The data for the new user.

        Returns:
            User: The newly created user object.
        """
        try:
            user = User(**user_data)
            self.session.add(user)
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def update_user(self, user_id, user_data):
        """
        Updates an existing user.

        Args:
            user_id (int): The ID of the user to update.
            user_data (dict): The updated data for the user.

        Returns:
            User: The updated user object.
        """
        try:
            user = self.get_user(user_id)
            if user:
                for key, value in user_data.items():
                    setattr(user, key, value)
                self.session.commit()
                return user
            else:
                raise ValueError("User not found")
        except Exception as e:
            self.session.rollback()
            raise e