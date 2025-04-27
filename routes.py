from flask import Blueprint, request, jsonify
from pydantic import BaseModel, EmailStr, Field, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from db.database import session_scope
from db.models import User

main_blueprint = Blueprint(name='main', import_name=__name__)

# Настройка Flask-Login
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    with session_scope() as session:
        user = session.query(User).get(int(user_id))
        if user:
            session.expunge(user)  # Отсоединяем объект от сессии
        return user

# Pydantic-схема для регистрации
class RegistrationData(BaseModel):
    username: str = Field(..., min_length=4, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=36)
    confirm_password: str

    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

# Pydantic-схема для логина
class LoginData(BaseModel):
    email: EmailStr
    password: str

@main_blueprint.route(rule='/register', methods=['POST'])
def register():
    try:
        # Получаем JSON-данные из тела запроса
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Валидируем данные через Pydantic
        registration_data = RegistrationData(**data)
        registration_data.validate_passwords()

        with session_scope() as session:
            # Проверяем, существует ли пользователь с таким email
            user = session.query(User).filter_by(email=registration_data.email).first()
            if user:
                return jsonify({"error": "User with this email already exists"}), 400

            # Проверяем, существует ли пользователь с таким username
            user = session.query(User).filter_by(username=registration_data.username).first()
            if user:
                return jsonify({"error": "User with this username already exists"}), 400

            # Создаем нового пользователя
            user = User(
                username=registration_data.username,
                email=registration_data.email,
                password_hash=generate_password_hash(registration_data.password)
            )
            session.add(user)

        return jsonify({"message": "User registered successfully"}), 201

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@main_blueprint.route(rule='/login', methods=['POST'])
def login():
    try:
        # Получаем JSON-данные из тела запроса
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Валидируем данные через Pydantic
        login_data = LoginData(**data)

        with session_scope() as session:
            user = session.query(User).filter_by(email=login_data.email).first()
            if user and check_password_hash(user.password_hash, login_data.password):
                login_user(user)
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"error": "Invalid email or password"}), 401

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@main_blueprint.route(rule='/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

@main_blueprint.route(rule='/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }), 200
