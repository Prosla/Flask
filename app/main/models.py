from peewee import CharField

from app.base_model import BaseModel


class User(BaseModel):
    name = CharField(max_length=100)
    email = CharField(max_length=150, unique=True, index=True)


class RegisteredUsers(BaseModel):
    name = CharField(max_length=15)
    email = CharField(max_length=50, unique=True, index=True)
    password = CharField(max_length=80, index=True)