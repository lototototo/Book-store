from flask import Blueprint, flash, redirect, url_for, render_template, request, jsonify
from pydantic import BaseModel, EmailStr, Field, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from db.database import session_scope
from db.models import User

main_blueprint = Blueprint(name='main', import_name=__name__)

# Pydantic-схема для регистрации
class RegistrationData(BaseModel):
    username: str = Field(..., min_length=4, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=36)
    confirm_password: str

    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

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
            user = session.query(User).filter_by(email=registration_data.email).first()
            if user:
                return jsonify({"error": "User with this email already exists"}), 400

            # Создаем нового пользователя
            user = User(
                username=registration_data.username,
                email=registration_data.email,
                password_hash=generate_password_hash(registration_data.password)
            )
            session.add(user)

        return jsonify({"message": "User registered successfully"}), 201

    except ValidationError as e:
        # Возвращаем ошибки валидации
        return jsonify({"errors": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@main_blueprint.route(rule='/login', methods=['POST'])
def login():
    try:
        # Pydantic-схема для логина
        class LoginData(BaseModel):
            email: EmailStr
            password: str

        # Получаем JSON-данные из тела запроса
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Валидируем данные через Pydantic
        login_data = LoginData(**data)

        with session_scope() as session:
            user = session.query(User).filter_by(email=login_data.email).first()
            if user and check_password_hash(user.password_hash, login_data.password):
                # Здесь можно добавить логику для создания сессии пользователя
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"error": "Invalid email or password"}), 401

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@main_blueprint.route(rule='/main')
def main_route():
    return render_template(template_name_or_list='home.html')
