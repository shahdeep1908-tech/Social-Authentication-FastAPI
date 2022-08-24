from database import Base, get_db
from sqlalchemy import Column, String, or_
from sqlalchemy.exc import SQLAlchemyError

"""
Contains User Table and different classmethod to perform database queries.
"""
db = next(get_db())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    profile_picture = Column(String(255), nullable=True)

    def save(self, db_session):
        db_session.add(self)
        db_session.commit()

    @classmethod
    def check_user_exists(cls, user):
        """
        Check user existence in the above user table.
        :param user: str - username/email as per social auth response
        :return: userdata if exists or None
        """
        return db.query(cls).filter(or_(cls.email == user, cls.username == user)).first()

    @classmethod
    def create_user(cls, user_id, username, email, picture):
        """
        Fetch new user data and perform insert operation in above user table.
        :param user_id: str - user social account ID
        :param username: str - social account username or None
        :param email: str - social account email or None
        :param picture: str - associated social account profile picture or None
        :return: userdata if inserted in db else SQLError
        """
        try:
            user = cls(id=user_id, username=username, email=email, profile_picture=picture)
            user.save(db)
            db.refresh(user)
            return user
        except SQLAlchemyError as e:
            return e

    @classmethod
    def get_user_data(cls, user):
        """
        Fetch user data, specifically for login user.
        :param user: str - email/username as per login token
        :return: userdata associated with above users table
        """
        return db.query(cls).filter(or_(cls.email == user, cls.username == user)).first()
