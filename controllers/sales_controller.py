from main import app
from flask import render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from flask_login import login_required
from models.Conexao import engine
from models.vendas_model import Venda  
from models.produto_model import Produto

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route('/vendas', methods=['GET'])
@login_required
def vendas_list():
    db = SessionLocal()
    vendas = db.query(Venda).all()
    return render_template("vendas.html", vendas=vendas)

@app.route('/vendas/search', methods=['POST'])
@login_required
def vendas_search():
    db = SessionLocal()
    cliente_nome = request.form['clienteNome']
    vendas = db.query(Venda).filter(Venda.cliente_nome.like(f"%{cliente_nome}%")).all()
    return render_template("vendas.html", vendas=vendas)

@app.route('/vendas/novo', methods=['GET'])
@login_required
def venda_novo():
    db = SessionLocal()
    produtos = db.query(Produto).all()
    return render_template("editarvendas.html", venda=Venda(cliente_nome="", total=0), produtos=produtos)


@app.route('/vendas/produto/<int:id>', methods=['GET'])
@login_required
def produto_preco(id):
    db = SessionLocal()
    produtos = db.query(Produto).get(id)
    if produtos != None:
        preco_formatado = f"{produtos.preco:,.2f}"
        return preco_formatado
    return ""



@app.route('/vendas/editar/<int:id>', methods=['GET'])
@login_required
def venda_editar(id):
    db = SessionLocal()
    venda = db.query(Venda).get(id)
    return render_template("editarvendas.html", venda=venda)

@app.route('/vendas/<int:id>', methods=['GET'])
@login_required
def venda_delete(id):
    db = SessionLocal()
    db.query(Venda).filter(Venda.id == id).delete()
    db.commit()
    msg = "Venda deletada com sucesso"
    return redirect(url_for('vendas_list', msg=msg))

@app.route('/vendas/salvar', methods=['POST'])
@login_required
def venda_save():
    db = SessionLocal()
    id = request.form['id']
    cliente_nome = request.form['clienteNome']
    total = request.form['total']
    total = total.replace(",", ".")
    print(total)
    idProduto = request.form['idProduto']
    
    if id == "":
        venda = Venda(cliente_nome=cliente_nome, total=total, idProduto=idProduto)
        db.add(venda)
        db.commit()
    else:
        venda = db.query(Venda).get(id)
        if venda:
            venda.cliente_nome = cliente_nome
            venda.total = total
            db.commit()
    
    return redirect(url_for('vendas_list', msg="Venda salva com sucesso!"))
