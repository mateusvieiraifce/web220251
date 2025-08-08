from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, logout_user
from models.Conexao import Base
from models.user_model import User

app = Flask(__name__)
#configura app e loginManagerment
app.secret_key = "SUA_CHAVE_CRIPT"
login_magengemnt = LoginManager()
login_magengemnt.init_app(app)
login_magengemnt.login_view = "login"

#configura o metodo load user
@login_magengemnt.user_loader
def load_user(user_id):
    db  = SessionLocal()
    return db.query(User).get(user_id)

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return render_template("login.html")

#de fato faz o login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = SessionLocal()
        user = db.query(User).where(User.login==username).first()
        if not user:
              return redirect(url_for('login', msg="usuário não encontrado"))
              #return render_template("login.html", msg="usuário não encontrado")
        else:
            if user.pasword == password:
                login_user(user)
                return redirect(url_for("index"))
            else:
                return redirect(url_for('login', msg="Senha inválida"))
    else:
        return render_template("login.html")


from controllers.produtos_controller import  *
from controllers.servicos_controller import *
from controllers.users_controller import  *
from controllers.sales_controller import *


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

    """Popula o banco de dados com dados iniciais"""
    db  = SessionLocal();
    
    # Limpa os dados existentes (opcional)
    #db.session.drop_all()
    #db.create_all()
    
    # Cria usuários de exemplo
    users = [
        User(nome='mentrixmax@gmail.com', login='mentrixmax@example.com' , password="123"),
    ]
    
    
    # Adiciona todos ao banco de dados
   # db.add_all(users)
    db.commit()


    app.run(debug=True, host='0.0.0.0', port=5001)
