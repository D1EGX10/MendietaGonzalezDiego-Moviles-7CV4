from datetime import datetime, timedelta, timezone
import os

import jwt
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY no está configurada. Crea un archivo .env basado en .env.example")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    tasks = db.relationship("Task", backref="owner", lazy=True, cascade="all, delete-orphan")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False, default="")
    completed = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2),
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")


def authenticated_user():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, (jsonify({"message": "Token requerido"}), 401)

    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        user = db.session.get(User, payload["user_id"])
        if user is None:
            return None, (jsonify({"message": "Usuario no encontrado"}), 401)
        return user, None
    except jwt.ExpiredSignatureError:
        return None, (jsonify({"message": "Token expirado"}), 401)
    except jwt.InvalidTokenError:
        return None, (jsonify({"message": "Token inválido"}), 401)


def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
    }


@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "API funcionando"}), 200


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    if not username or not password:
        return jsonify({"message": "username y password son obligatorios"}), 400

    if len(password) < 6:
        return jsonify({"message": "La contraseña debe tener al menos 6 caracteres"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "El usuario ya existe"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401

    return jsonify({
        "status": "success",
        "message": "Login exitoso",
        "user_id": user.id,
        "username": user.username,
        "token": create_token(user.id),
    }), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    user, error = authenticated_user()
    if error:
        return error

    tasks = Task.query.filter_by(user_id=user.id).all()
    return jsonify([task_to_dict(task) for task in tasks]), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    user, error = authenticated_user()
    if error:
        return error

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if task is None:
        return jsonify({"message": "Tarea no encontrada"}), 404

    return jsonify(task_to_dict(task)), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    user, error = authenticated_user()
    if error:
        return error

    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    description = str(data.get("description", "")).strip()
    completed = bool(data.get("completed", False))

    if not title:
        return jsonify({"message": "title es obligatorio"}), 400

    task = Task(
        title=title,
        description=description,
        completed=completed,
        user_id=user.id,
    )
    db.session.add(task)
    db.session.commit()

    return jsonify(task_to_dict(task)), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    user, error = authenticated_user()
    if error:
        return error

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if task is None:
        return jsonify({"message": "Tarea no encontrada"}), 404

    data = request.get_json(silent=True) or {}
    if "title" in data:
        title = str(data["title"]).strip()
        if not title:
            return jsonify({"message": "title no puede estar vacío"}), 400
        task.title = title
    if "description" in data:
        task.description = str(data["description"]).strip()
    if "completed" in data:
        task.completed = bool(data["completed"])

    db.session.commit()
    return jsonify(task_to_dict(task)), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    user, error = authenticated_user()
    if error:
        return error

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if task is None:
        return jsonify({"message": "Tarea no encontrada"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tarea eliminada"}), 200


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
