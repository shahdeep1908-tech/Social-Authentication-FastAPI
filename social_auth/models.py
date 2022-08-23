from database import Base, get_db
from sqlalchemy import Column, String, or_
from sqlalchemy.exc import SQLAlchemyError

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
        return db.query(cls).filter(or_(cls.email == user, cls.username == user)).first()

    @classmethod
    def create_user(cls, user_id, username, email, picture):
        try:
            user = cls(id=user_id, username=username, email=email, profile_picture=picture)
            user.save(db)
            db.refresh(user)
            return user
        except SQLAlchemyError as e:
            return e

    @classmethod
    def get_user_data(cls, user):
        return db.query(cls).filter(or_(cls.email == user, cls.username == user)).first()
