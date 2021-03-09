import logging
from datetime import datetime, timedelta, timezone
from flask import Blueprint, redirect, request, url_for, make_response, flash, render_template
from flask_jwt_extended import create_access_token, verify_jwt_in_request, \
    set_access_cookies, get_current_user, unset_jwt_cookies, get_jwt
from jwt.exceptions import ExpiredSignatureError

from control_panel import bcrypt, db
from control_panel.models import User
from control_panel.main.forms import LoginForm, RegistrationForm

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return "Welcome to Compal Control Panel"


@main.route('/cloud_resource')
def cloud_resource():
    identity, unset = is_authenticated()
    print(identity)
    if not identity:
        flash('Please login first', 'danger')
        return redirect(url_for('main.login'))
    return render_template('index.html', identity=identity, page="cloud_resource")


@main.route('/terminal_connection')
def terminal_connection():
    identity, unset = is_authenticated()
    print(identity)
    if not identity:
        flash('Please login first', 'danger')
        return redirect(url_for('main.login'))
    return render_template('terminal_connection.html', identity=identity, page="terminal_connection")


@main.route('/content_management')
def content_management():
    identity, unset = is_authenticated()
    print(identity)
    if not identity:
        flash('Please login first', 'danger')
        return redirect(url_for('main.login'))
    return render_template('content_management.html', identity=identity, page="content_management")


@main.route("/user_management")
def user_management():
    identity, unset = is_authenticated()
    print(identity)
    if not identity:
        flash('Please login first', 'danger')
        return redirect(url_for('main.login'))
    return render_template('user_management.html', identity=identity, page="user_management")


@main.route("/system")
def system_setting():
    identity, unset = is_authenticated()
    print(identity)
    if not identity:
        flash('Please login first', 'danger')
        return redirect(url_for('main.login'))
    return render_template('system.html', identity=identity, page="system")


@main.route('/login', methods=['GET', 'POST'])
def login():
    identity, unset = is_authenticated()
    if identity:
        return redirect(url_for('main.cloud_resource'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        try:
            user = User.query.filter_by(username=username).one_or_none()
            if user and bcrypt.check_password_hash(user.password, password):
                access_token = create_access_token(identity=user)
                resp = redirect(url_for('main.cloud_resource'))
                next_page = request.args.get('next')
                if next_page:
                    resp = redirect(next_page)
                set_access_cookies(resp, access_token)
                return resp
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        except Exception as inst:
            logging.debug(inst)
            flash('Internal server error. Please try again later', 'danger')

    resp = make_response(
        render_template('login.html', title='Login', form=login_form))
    if unset:
        unset_jwt_cookies(resp)

    return resp


@main.route('/register', methods=['GET', 'POST'])
def register():
    identity, unset = is_authenticated()
    if identity:
        return redirect(url_for('main.cloud_resource'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    resp = make_response(render_template('register.html', title='Register', form=form))
    if unset:
        unset_jwt_cookies(resp)
    return resp


@main.route('/logout')
def logout():
    resp = redirect(url_for('main.login'))
    unset_jwt_cookies(resp)
    return resp


@main.route('/db')
def db_sync():
    db.create_all()
    db.session.commit()

    return "DB sync"


# refresh token
@main.after_request
def refresh_expiring_jwt(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_current_user())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


def is_authenticated():
    unset = False
    try:
        verify_jwt_in_request(optional=True)
        if get_current_user():
            identity = get_current_user()
            return identity, unset
    except ExpiredSignatureError as inst:
        flash('Token expired. Please login again', 'danger')
        print(inst)
        unset = True

    except Exception as inst:
        logging.debug(inst, type(inst))

    return None, unset
