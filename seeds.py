from controllers.produtos_controller import SessionLocal
from main import app
import click
from models.produto_model import Produto   # Importe seus modelos
from models.user_model import User

def seed_db():
    """Popula o banco de dados com dados iniciais"""
    db  = SessionLocal();
    
    # Limpa os dados existentes (opcional)
    db.drop_all()
    db.create_all()
    
    # Cria usuários de exemplo
    users = [
        User(nome='mentrixmax@gmail.com', login='mentrixmax@example.com' , password="123"),
    ]
    
    # Adiciona produtos de exemplo
    products = [
        Product(name='Produto A', price=10.99),
        Product(name='Produto B', price=24.50),
        Product(name='Produto C', price=35.75)
    ]
    
    # Adiciona todos ao banco de dados
    db.session.add_all(users + products)
    db.session.commit()
    
    click.echo(f"Seed completado! {len(users)} usuários e {len(products)} produtos criados.")