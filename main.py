from flask import Flask, render_template, request

from models.Conexao import Base

app = Flask(__name__)

from controllers.produtos_controller import  *


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run(debug=True, host='0.0.0.0', port=5001)
