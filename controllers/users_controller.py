from main import app
from flask import render_template, request, jsonify, redirect, url_for
from sqlalchemy.orm import sessionmaker

from models.Conexao import engine
from models.produto_model import Produto
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route('/users', methods=['GET'])
def usuarios_list():

    return render_template("usuarios.html")
