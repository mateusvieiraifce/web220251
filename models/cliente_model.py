

from sqlalchemy import Column, Integer, String, Float

from models.Conexao import Base, engine


class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

    def __init__(self, nome, email, endereco):
        self.nome = nome
        self.email = email
        self.endereco = endereco
        self.id = None

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "endereco": self.endereco,
        }
