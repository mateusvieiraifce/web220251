

from sqlalchemy import Column, Integer, String, Float

from models.Conexao import Base, engine
from sqlalchemy.orm import relationship

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    vendas = relationship("Venda", back_populates="produto")
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
