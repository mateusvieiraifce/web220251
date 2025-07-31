from main import app
from flask import render_template, request, jsonify, redirect, url_for
from sqlalchemy.orm import sessionmaker

from models.Conexao import engine
from models.produto_model import Produto
from models.servico_model import Servico
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route('/servicos', methods=['GET'])
def servicos_list():
    db = SessionLocal()
    servicos = db.query(Servico).all()
    return render_template("servicos.html", servicos=servicos)

@app.route('/servicos/search', methods=['POST'])
def servicos_searchs():
    db = SessionLocal()
    nome = request.form['servicoNome']
    servicos = db.query(Servico).where(Servico.nome.like("%"+nome+"%"))
    return render_template("servicos.html", servicos=servicos)

@app.route('/servicos/<int:id>', methods=['GET'])
def servico_delete(id):
    db = SessionLocal()
    db.query(Servico).filter(Servico.id == id).delete()
    db.commit()
    msgI = "Servico deletado com sucesso"
    return redirect(url_for('servicos_list', msg=msgI))

@app.route('/servicos/novo', methods=['GET'])
def servico_novo():
    return render_template("editarservicos.html",serv=Servico(nome="", preco=0))

@app.route('/servicos/editar/<int:id>', methods=['GET'])
def servico_editar(id):
    db = SessionLocal()
    serv = db.query(Servico).get(id)
    return render_template("editarservicos.html",serv=serv)

@app.route('/servicos/salvar', methods=['POST'])
def servico_save():
    db = SessionLocal()
    nome = request.form['servicoNome']
    preco = request.form['preco']
    id = request.form['id']
    preco = preco.replace(".", "")
    preco = preco.replace(",", ".")
    if id is "":
        print("chegou aqui" + id)
        servico = Servico(nome=nome, preco=preco)
        db.add(servico)
        db.commit()
    else:
       servico =  db.query(Servico).get(id)
       if servico:
            servico.preco = preco
            servico.nome = nome
            db.commit()
    return redirect(url_for('servicos_list', msg="Serviço Salvo com sucesso!!"))