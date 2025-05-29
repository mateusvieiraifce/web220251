from main import app
from flask import render_template, request, jsonify, redirect, url_for
from sqlalchemy.orm import sessionmaker

from models.Conexao import engine
from models.produto_model import Produto

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# exemplo de uma rota devolvendo apenas um texto.

@app.route('/produtos/novo', methods=['GET'])
def produto_novo():
    #vamos no banco de dados,
    #depois consultamos todos
    #depois passamos pra view
    #naview agente monta a tabela
    db = SessionLocal()
    produtos = db.query(Produto).all()
    return render_template("produtos.html",prd=produtos)

@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return 'Hello World!'

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
        id = request.form['id']
        db = SessionLocal()
        if id == "":
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


# exemplo de uma rota que trata dados de um formulário html
@app.route('/novo', methods=['POST'])
def hello_world_k():  # put application's code here
    #acessar o BD e salvar essa informação no BD
    #funcao do banck-end, receber os dados, tratar, fazer validações, pessitir os dados
    # recuperar dados perssitidos.

    return 'novo PWII' + request.form['nome'] + request.form['aniversario']

@app.route('/produtos/listar', methods=['GET'])
def produto_lista():
    db = SessionLocal()
    produtos = db.query(Produto).all()
    return jsonify([produto.to_dict() for produto in produtos]), 200

@app.route('/produtos/deletar/<int:id>', methods=['GET'])
def produto_deletar(id):
    # id = request.form['id']
     db = SessionLocal()
     produto = db.query(Produto).filter_by(id=id).first()
     if produto is None:
         return jsonify({'msg': 'produto nao encontrado'}), 404
     else:
         db.delete(produto)
         db.commit()
         return jsonify({"mensagem": "Produto deletado!"})

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
