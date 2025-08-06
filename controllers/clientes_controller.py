from main import app
from flask import render_template, request, jsonify, redirect, url_for
from sqlalchemy.orm import sessionmaker

from models.Conexao import engine
from models.cliente_model import Cliente
from flask_login import login_required

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.route('/clientes', methods=['GET'])
@login_required
def cliente_novo():
    perPage = 5
    page = request.args.get('page', 1, type=int)
    db = SessionLocal()
    try:
        clientes = db.query(Cliente).order_by(Cliente.nome).offset((page - 1) * perPage).limit(perPage).all()
        total = db.query(Cliente).count()
        nPages = (total // perPage) + (1 if total % perPage else 0)
        if nPages == 0:
            nPages = 1
        return render_template("clientes.html", prd=clientes, page=page, nPages=nPages)
    finally:
        db.close()


@app.route('/clientes/novo', methods=["GET"])
@login_required
def cliente_new():
    cliente = Cliente(nome="", email="", endereco="")
    cliente.id = ""
    return render_template("editarcliente.html", prd=cliente)


@app.route('/clientes/salvar', methods=['POST'])
@login_required
def cliente_salvar():
    msgI = "Operação realizada com sucesso!!"
    db = SessionLocal()
    try:
        nome = request.form['nomecliente']
        email = request.form['emailcliente']
        endereco = request.form['enderecocliente']
        id = request.form['id']

        if id == "":
            prd = Cliente(nome=nome, email=email, endereco=endereco)
            db.add(prd)
        else:
            prd = db.get(Cliente, int(id))
            prd.nome = nome
            prd.email = email
            prd.endereco = endereco
        db.commit()
    except Exception as e:
        db.rollback()
        msgI = "Operação não realizada, verifique os campos"
        print(e)
    finally:
        db.close()
    return redirect(url_for('cliente_lista', msg=msgI))


@app.route('/clientes/listar', methods=['GET'])
@login_required
def cliente_lista():
    db = SessionLocal()
    try:
        nome = request.args.get('nome', "")
        page = int(request.args.get('page', 1))
        perPage = 5

        total = db.query(Cliente).filter(Cliente.nome.like(f"%{nome}%")).count()
        nPages = total // perPage + (1 if total % perPage != 0 else 0)
        if nPages == 0:
            nPages = 1
        if page > nPages:
            page = nPages

        clientes = db.query(Cliente)\
            .filter(Cliente.nome.like(f"%{nome}%"))\
            .order_by(Cliente.nome)\
            .offset((page - 1) * perPage)\
            .limit(perPage).all()

        return render_template("clientes.html", prd=clientes, nome=nome, page=page, total=total, nPages=nPages)
    finally:
        db.close()


@app.route('/clientes/deletar/<int:id>', methods=['GET'])
@login_required
def cliente_deletar(id):
    db = SessionLocal()
    try:
        cliente = db.query(Cliente).filter_by(id=id).first()
        if cliente is None:
            msgI = "Cliente não encontrado"
        else:
            db.delete(cliente)
            db.commit()
            msgI = "Cliente deletado com sucesso"
    except Exception as e:
        db.rollback()
        print(e)
        msgI = "Erro ao deletar cliente"
    finally:
        db.close()
    return redirect(url_for('cliente_lista', msg=msgI))


@app.route('/clientes/editar/<int:id>', methods=["GET"])
@login_required
def cliente_edit(id):
    db = SessionLocal()
    try:
        cliente = db.get(Cliente, id)
        return render_template("editarcliente.html", prd=cliente)
    finally:
        db.close()
