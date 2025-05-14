from flaskavel.lab.reagents.hash import Hash
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email_verified_at = Column(DateTime, default=None)
    remember_token = Column(String(100), default=None)

    # Define a hybrid property for casting `password`
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        # Here, you should hash the password before storing it
        self._password = Hash.make(value)

    @validates('email')
    def validate_email(self, key, email):
        # Add your validation logic for email
        if '@' not in email:
            raise ValueError("Invalid email address")
        return email