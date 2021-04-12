from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from friendshipStatus import Status


class BaseEntity:
    id = db.Column(db.Integer, primary_key=True)


class Route(db.Model, BaseEntity):
    __tablename__ = "routes"
    start_from = db.Column(db.String)
    end_to = db.Column(db.String)
    posts = db.relationship('Post', backref='route')
    cycle_parties = db.relationship('CycleParty', backref='route')


# User shouldn't go in db?


class User(db.Model, BaseEntity):
    __tablename__ = "users"
    name = db.Column(db.String(35))
    username = db.Column(db.String(35))
    email = db.Column(db.String(35))
    password = db.Column(db.String(35))
    friends = db.relationship('Friend', backref='user')
    friend_requests = db.relationship('FriendRequest', backref='user')
    cycled_routes = db.relationship('CycledRoute', backref='user')
    posts = db.relationship('Post', backref='user')
    messages = db.relationship('Message', backref='user')
    party_member = db.relationship('CyclePartyMember', backref='user', useList=False)


class Friend(db.Model, BaseEntity):
    __tablename__ = "friends"
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    became_friends_on = db.Column(DateTime)


class FriendRequest(db.Model, BaseEntity):
    __tablename__ = "friend_requests"
    from_userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    friend_request_date = db.Column(DateTime, default=datetime.utcnow)
    is_confirmed = db.Column(db.Boolean)
    status = db.Column(db.String)


class Message(db.Model, BaseEntity):
    __tablename__ = "messages"
    from_userid = db.Column(db.Integer, db.ForeignKey('users.id'))  # ??
    to_userid = db.Column(db.Integer, db.ForeignKey('users.id'))  # ??
    text = db.Column(db.String)
    sent_on = db.Column(DateTime)
    is_seen = db.Column(db.Boolean)
    time_seen = db.Column(db.DateTime)


class CycledRoute(db.Model, BaseEntity):
    __tablename__ = 'cycled_routes'
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    distanceTravelled = db.Column(db.String)
    caloriesBurned = db.Column(db.Integer)
    location_from_id = db.Column(db.Integer, Route.id)
    location_to_id = db.Column(db.Integer, Route.id)
    post = db.Column(db.Integer, db.ForeignKey('posts.id'))


class Post(db.Model, BaseEntity):
    __tablename__ = "posts"
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.String)
    type = db.Column(db.String)
    image = db.Column(db.String)
    route = db.relationship('CycledRoute', backref='post', useList=False)
    created_on = db.Column(DateTime)
    comments = db.relationship("Comment", backref='post')


class Comment(db.Model, BaseEntity):
    __tablename__ = 'comments'
    postId = db.Column(db.Integer, db.ForeignKey('posts.id'))
    userId = db.Column(db.Integer)
    text = db.Column(db.String)
    created_on = db.Column(DateTime)


class Location(db.Model, BaseEntity):
    __tablename__ = "locations"
    userId = db.Column(db.Integer)  # ??
    longitude = db.Column(db.String)
    latitude = db.Column(db.String)


class CycleParty(db.Model, BaseEntity):
    __tablename__ = "cycle_parties"
    route = db.Column(db.Integer, db.ForeignKey('routes.id'))
    partyCreatorId = db.Column(db.Integer)
    cycle_party_members = db.relationship('CyclePartyMember', backref='CycleParty')


class CyclePartyMember(db.Model, BaseEntity):
    __tablename__ = "cycle_party_members"
    partyId = db.Column(db.Integer, db.ForeignKey('cycle_parties.id'))
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
