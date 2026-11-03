from flask import Flask, Response, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from db import Session, User
from errors import HttpError
from schema import CreateUser, UpdateUser, validate

app = Flask("app")
bcrypt = Bcrypt(app)


def hash_password(password: str) -> str:
    password = password.encode()
    password = bcrypt.generate_password_hash(password)
    password = password.decode()
    return password


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_requests(response: Response):
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    response = jsonify({"error": err.message})
    response.status_code = err.status_code
    return response


def hello_world(some_id):
    json_data = request.json
    qs = request.args
    headers = request.headers
    print(f"{json_data=}")
    print(f"{qs=}")
    print(f"{headers=}")

    response = jsonify({"hello": "world"})
    response.status_code = 201
    return response


def get_user(user_id: int) -> User:
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError("user not found", 404)
    return user


def add_user(user: User):
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError("user already exists", 400)


class UserView(MethodView):
    def get(self, user_id):
        user = get_user(user_id)
        return jsonify(user.dict)

    def post(self):
        json_data = validate(request.json, CreateUser)
        user = User(
            name=json_data["name"], password=hash_password(json_data["password"])
        )
        add_user(user)
        return jsonify(user.id_dict)

    def patch(self, user_id):
        json_data = validate(request.json, UpdateUser)
        user = get_user(user_id)
        if "name" in json_data:
            user.name = json_data["name"]
        if "password" in json_data:
            user.password = hash_password(json_data["password"])
        add_user(user)
        return jsonify(user.dict)

        pass

    def delete(self, user_id):

        user = get_user(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"message": "deleted"})


user_view = UserView.as_view("user")

app.add_url_rule("/hello/world/<int:some_id>", view_func=hello_world, methods=["POST"])
app.add_url_rule("/users", view_func=user_view, methods=["POST"])
app.add_url_rule(
    "/users/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)


app.run()
