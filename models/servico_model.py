

from sqlalchemy import Column, Integer, String, Float

from models.Conexao import Base, engine


class Servico(Base):
    __tablename__ = 'servico'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco
        self.id = None

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
        }
