from sqlalchemy import Column, Integer, String, Float, ForeignKey

from models.Conexao import Base ,engine
from sqlalchemy.orm import relationship

class Venda(Base):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True, index=True)
    cliente_nome = Column(String)
    total = Column(Float)
    idProduto = Column(Integer, ForeignKey('produtos.id')) 

    produto = relationship("Produto", back_populates="vendas")
