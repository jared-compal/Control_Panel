from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required, get_current_user, \
    create_refresh_token, create_access_token

from control_panel import db, bcrypt
from control_panel.models import User

auth_service = Blueprint('auth_service', __name__)


@auth_service.route('/user_login', methods=['POST'])
def user_login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    return user_authenticate(username, password)


@auth_service.route("/user_logout")
def user_logout():
    return jsonify({
        "status": True,
        "msg": "Successfully log out user",
        "access_token": None
    })


@auth_service.route('/user_register', methods=['POST'])
def user_register():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    return validate_username(username, password)


@auth_service.route('/protected')
@jwt_required()
def protected_content():
    return jsonify(
        id=current_user.id,
        username=current_user.username
    )


@auth_service.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    identity = get_current_user()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


def user_authenticate(username, password):
    user = User.query.filter_by(username=username).one_or_none()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        return jsonify({
            "status": True,
            "msg": "Successfully log in user",
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    else:
        return jsonify({
            'status': False,
            'msg': 'Login Unsuccessful. Please check username and password'
        })


def validate_username(username, password):
    msg = "That username is taken. Please choose a different one."
    status = False
    if not User.query.filter_by(username=username).first():
        msg = "Successfully create user"
        status = True
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
    return jsonify({
        "status": status,
        "msg": msg
    })
