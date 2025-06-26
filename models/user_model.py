

from sqlalchemy import Column, Integer, String, Float

from models.Conexao import Base, engine
from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    login = Column(String, nullable=False)
    pasword = Column(String, nullable=False)

    def __init__(self, nome, login, password):
        self.nome = nome
        self.login = login
        self.pasword = password

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "login": self.login,
        }
