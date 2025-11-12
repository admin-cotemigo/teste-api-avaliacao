# config.py
import os
import connexion
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from connexion.exceptions import ProblemException

BASE_DIR = os.path.dirname(__file__)
SPEC_DIR = os.path.join(BASE_DIR, "openapi_specs")

# Usa caminho absoluto para evitar falhas de import no Heroku
vuln_app = connexion.App(__name__, specification_dir=SPEC_DIR)

# Banco: cria diretório se não existir (evita erro no primeiro boot)
DB_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DB_DIR, exist_ok=True)
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(DB_DIR, "database.db")
vuln_app.app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
vuln_app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
vuln_app.app.config["SECRET_KEY"] = "random"

db = SQLAlchemy(vuln_app.app)

def custom_problem_handler(error):
    from flask import jsonify
    response = jsonify({
        "status": "fail",
        "message": getattr(error, "detail", "An error occurred"),
    })
    response.status_code = error.status
    return response

vuln_app.add_error_handler(ProblemException, custom_problem_handler)

# Só depois de configurar tudo, carrega a especificação
vuln_app.add_api("openapi3.yml")

# exporta o WSGI app se quiser apontar Procfile para config:app
app = vuln_app.app
