from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from friendshipStatus import Status
import uuid

class Friends(db.Model):
    __tablename__ = 'friends'
    user1Id = db.Column(db.BigInteger, nullable = False, primary_key = True)
    user2Id = db.Column(db.BigInteger, nullable = False, primary_key = True)

class FriendRequest(db.Model):
    __table__name = 'friend_requests'
    fromUserId = db.Column(db.BigInteger, nullable = False, primary_key = True)
    toUserId = db.Column(db.BigInteger, nullable = False, primary_key = True)
    status = db.Column(db.Enum(Status), default = Status.PENDING)

class Message(db.Model):
    __tablename__ = 'messages'
    fromUserId = db.Column(db.BigInteger, nullable = False, primary_key = True)
    toUserId = db.Column(db.BigInteger, nullable = False, primary_key = True)
    dateSent = db.Column(db.DateTime, nullable = False, primary_key = True)
    text = db.Column(db.String, nullable = False)

class Post(db.Model):
    __tablename__ = 'posts'
    generatedId = str(uuid.uuid4().hex)
    id = db.Column(db.String, nullable = False ,default=generatedId, primary_key = True)
    userId = db.Column(db.BigInteger, nullable = False)
    text = db.Column(db.String, nullable = False)
    # image ?
    comments = db.relationship("Comment", backref = 'post')
    createdOn = db.Column(db.Date)

class Comment(db.Model):
    __tablename__ = 'comments'
    generatedId = str(uuid.uuid4().hex)
    id = db.Column(db.String, nullable = False ,default=generatedId, primary_key = True)
    postId = db.Column(db.String, db.ForeignKey('posts.id'))
    userId = db.Column(db.BigInteger, nullable = False)
    text = db.Column(db.String, nullable = False)
    createdOn = db.Column(db.DateTime)

class Route(db.Model):
    __tablename__ = 'route'
    generatedId = str(uuid.uuid4().hex)
    id = db.Column(db.String, nullable = False ,default=generatedId, primary_key = True)
    lng = db.Column(db.String, nullable = False)
    lat = db.Column(db.String, nullable = False)

class CycledRoute(db.Model):
    __tablename__ = 'cycled_routes'
    generatedId = str(uuid.uuid4().hex)
    id = db.Column(db.String, nullable = False ,default=generatedId, primary_key = True)
    #the userId here is needed to see each user's cycled routes
    userId = db.Column(db.BigInteger, nullable = False, primary_key = True)
    distanceTraveled = db.Column(db.String, nullable = False)
    caloriesBurned = db.Column(db.BigInteger)
    route = db.Column(db.String, db.ForeignKey('route.id'), nullable = False)

class CycleParty(db.Model):
    __tablename__ = 'cycle_party'
    generatedId = str(uuid.uuid4().hex)
    id = db.Column(db.String, nullable = False ,default=generatedId, primary_key = True)
    route = db.Column(db.String, db.ForeignKey('route.id'), nullable = False)
    partyCreatorId = db.Column(db.BigInteger, nullable = False)
    members = db.relationship("CyclePartyMember", backref = 'post')

class CyclePartyMember(db.Model):
    __tablename__ = 'cycle_party_member'
    partyId = db.Column(db.String, db.ForeignKey('cycle_party.id'), nullable = False, primary_key = True)
    userId = db.Column(db.BigInteger, nullable = False, primary_key = True)
