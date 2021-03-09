from datetime import datetime
from flask import jsonify
from control_panel import db, jwt


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify(code="Expired", err="Token expired, please refresh token"), 401


favorite_game_list = \
    db.Table('myFavorite',
             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
             db.Column('game_id', db.String(32), db.ForeignKey('game_list.game_id'))
             )


# Table of Game servers
class GameServers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_ip = db.Column(db.String(80), unique=True, nullable=False)
    client_ip = db.Column(db.String(80), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    last_connection_at = db.Column(db.DateTime, nullable=True)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    db_available_games = db.relationship("AvailableGamesForServers", backref="server")

    def __repr__(self):
        return '<Gserver id:{0} ip:{1}>'.format(self.id, self.server_ip)


class AvailableGamesForServers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(32), nullable=False)
    server_ip = db.Column(db.String(80), db.ForeignKey('game_servers.server_ip'), nullable=False)


class StreamList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_ip = db.Column(db.String(32), unique=True, nullable=False)
    client_ip = db.Column(db.String(32), unique=True, nullable=False)
    client_username = db.Column(db.String(64), nullable=True)
    stream_title = db.Column(db.String(128), nullable=False)
    num_of_audience = db.Column(db.Integer, default=0)
    img_url = db.Column(db.String(512))
    stream_url = db.Column(db.String(512))
    video_source_url = db.Column(db.String(512), nullable=True)
    started_from = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class GameList(db.Model):
    id = db.Column(db.Integer, unique=True, autoincrement=True)
    game_id = db.Column(db.String(32), primary_key=True, nullable=False)
    game_title = db.Column(db.String(32), nullable=False)
    game_type = db.Column(db.String(32))
    game_brief = db.Column(db.String(256))
    img_url = db.Column(db.String(256))
    users = db.relationship('User', secondary=favorite_game_list, backref='games')


class ClientConnectionList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), unique=False, nullable=True)
    client_ip = db.Column(db.String(32), unique=False, nullable=False)
    server_ip = db.Column(db.String(32), unique=False, nullable=False)
    game_id = db.Column(db.String(32), unique=False, nullable=False)
    connection_status = db.Column(db.String(32), nullable=False)
    launch_time = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    close_time = db.Column(db.DateTime, nullable=True)
    total_play_time = db.Column(db.BigInteger, nullable=True,
                                default=0)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    delete_flag = db.Column(db.Boolean(), nullable=False, default=False)
    roles = db.relationship('Role', secondary='user_roles')
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
