from main import app
from flask import render_template, request, jsonify, redirect, url_for
from sqlalchemy.orm import sessionmaker

from models.Conexao import engine
from models.produto_model import Produto
from flask_login import login_required

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# exemplo de uma rota devolvendo apenas um texto.

@app.route('/produtos', methods=['GET'])
@login_required
def produto_novo():
    perPage =5
    page = request.args.get('page', 1, type=int)
    db = SessionLocal()
    produtos = db.query(Produto).order_by(Produto.nome).offset((page-1)*perPage).limit(perPage).all()
    total = db.query(Produto).where(Produto.nome.like(f"%%")).count()
    nPages = int(total / perPage)
    nPages = nPages + 2
    return render_template("produtos.html",prd=produtos, page=page, nPages=nPages)

@app.route('/', methods=['GET'])
def index():  # put application's code here
    return render_template("index.html")

# exemplo de uma rota que devolve um pagina de um template.
@app.route('/pagina', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/produtos/salvar', methods=['POST'])
def produto_salvar():
    msgI ="Operação realizada com sucesso!!"
    try:
        nome =  request.form['nomeproduto']
        preco = request.form['precos']
        preco = preco.replace(".","")
        preco = preco.replace(",",".")

        id = request.form['id']
        print("id vindo"+str(id))
        db = SessionLocal()
        if id is "":
            prd = Produto(nome, preco)
            db.add(prd)
        else:
            prd = db.query(Produto).get(id)
            prd.nome = nome
            prd.preco = preco
        db.commit()
    except Exception as e:
        msgI= "Operção nao realizada, verifique os campos"
        print(e)
    return redirect(url_for('produto_novo', msg=msgI))
     # salvar no bd
   #return "Salvo com sucesso"+str(prd.id)
@app.route('/produtos/editar/<int:id>', methods=["GET"])
def edit(id):
    db = SessionLocal()
    produto = db.query(Produto).get(id)
    return render_template("editarproduto.html", prd=produto)


@app.route('/produtos/novo', methods=["GET"])
def product_new():
    db = SessionLocal()
    produto = Produto(nome="", preco=0)
    produto.id = ""
    return render_template("editarproduto.html", prd=produto)


# exemplo de uma rota que trata dados de um formulário html
@app.route('/novo', methods=['POST'])
def hello_world_k():  # put application's code here
    #acessar o BD e salvar essa informação no BD
    #funcao do banck-end, receber os dados, tratar, fazer validações, pessitir os dados
    # recuperar dados perssitidos.

    return 'novo PWII' + request.form['nome'] + request.form['aniversario']

@app.route('/produtos/listar', methods=['POST'])
def produto_lista():
    db = SessionLocal()
    nome = request.form['nomeproduto']
    perPage = 5
    if request.form['page']!="":
        page = int(request.form['page'])
    else:
        page = 1
    db = SessionLocal()
    #produtos = db.query(Produto).order_by(Produto.nome).offset((page - 1) * perPage).limit(perPage).all()
    produtos = db.query(Produto).where(Produto.nome.like("%"+nome+"%")).order_by(Produto.nome).offset((page - 1) * perPage).limit(perPage).all()
    total = db.query(Produto).where(Produto.nome.like(f"%{nome}%")).count()
    nPages = int( total/perPage)
    nPages=nPages+2
    print("total"+str(total))
    print("nPages"+str(nPages))
    return render_template("produtos.html",prd=produtos,
                           nome=nome, page=page, total=total, nPages=nPages)

@app.route('/produtos/deletar/<int:id>', methods=['GET'])
def produto_deletar(id):
    # id = request.form['id']
     db = SessionLocal()
     produto = db.query(Produto).filter_by(id=id).first()
     if produto is None:
         msgI= "Produto não encontrado"
         return redirect(url_for('produto_novo', msg=msgI))
     else:
         db.delete(produto)
         db.commit()
         msgI= "Produto deletar com sucesso"
         return redirect(url_for('produto_novo', msg=msgI))
#implementando arquitetura rest
@app.route('/v1/products', methods=['GET'])
def product_list():
    db = SessionLocal()
    produtos = db.query(Produto).all()
    return jsonify([produto.to_dict() for produto in produtos]), 200

@app.route('/v1/products/<int:id>', methods=['GET'])
def product_get(id):
    db = SessionLocal()
    produto = db.query(Produto).get(id)
    if produto is None:
        return jsonify({'msg': 'produto nao encontrado'}), 404
    return jsonify(produto.to_dict()), 200

@app.route('/v1/products/<int:id>', methods=["DELETE"])
def product_delete(id):
    db = SessionLocal()
    prd = db.query(Produto).get(id)
    if prd is None:
        return jsonify({'msg': 'produto nao encontrado'}), 404
    else:
        db.delete(prd)
        db.commit()
        return jsonify({'msg': 'Produto Excluido com suceso'}), 204

@app.route('/v1/products', methods=['POST'])
def product_save():
    data = request.get_json()
    produto = Produto(nome= data['name'], preco=data['price'])
    db = SessionLocal()
    db.add(produto)
    db.commit()
    return jsonify(produto.to_dict()), 201

@app.route('/v1/products/<int:id>', methods=['PUT'])
def product_update(id):
    data = request.get_json()
    db = SessionLocal()
    produto = db.query(Produto).get(id)

    if produto is None:
        return jsonify({'msg': 'produto nao encontrado'}), 404

    produto.preco = data['price']
    produto.nome = data['name']
    db.commit()
    return jsonify(produto.to_dict()), 200


