import connexion
from sqlalchemy import or_
from flask import jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
from datetime import datetime
import math


def saveUserLocation(locationBody):
    new_location = Location(
        lng=locationBody['lng'],
        lat=locationBody['lat'],
        userId=locationBody['userId']
    )
    db.session.add(new_location)
    db.session.commit()
    return True


# get from user ms
# def get_all_users_key_value_from_user_ms(users_listBody):
#    users_list = []

def get_all_user_friends(user_id):
    user_friends_list = db.session.query(Friends).filter_by(user1Id=user_id).all()
    friends_list = []
    for friend in user_friends_list:
        friends_list.append({"user1Id": friend.user1Id, "user2Id": friend.user2Id})
    return {'friends': friends_list}


def get_user_timeline(user_id):
    # user_feed = Post.query.filter_by(userId=user_id).all()
    user_feed = db.session.query(Post).filter_by(userId=user_id).all()
    user_post_feed = []
    post_comments = []
    for post in user_feed:
        for comments in post.comments:
            post_comments.append({'commentId': comments.id, 'text': comments.text})
            print(comments.text)
        user_post_feed.append({'userId': post.userId, 'text': post.text, 'comments': post_comments})
        post_comments = []
    return {'timeline': user_post_feed}


def get_global_feed(user_id):
    posts = []
    user_posts = []
    friends = db.session.query(Friends).filter(or_(user1Id=user_id, user2Id=user_id)).all()
    for friend in friends:
        friend_id = friend['user1Id']
        friend_id2 = friend['user2Id']
        if friend_id != user_id:
            posts = db.session.query(Post).filter_by(userId=friend_id).all()
        if friend_id2 != user_id:
            posts = db.session.query(Post).filter_by(userId=friend_id2).all()
        for post in posts:
            user_posts.append({'userId': post.userId, 'text': post.text, 'comments': post.comments})

    return {'posts': user_posts}


def get_all_user_friend_requests(user_id):
    reqs = db.session.query(FriendRequest).filter_by(toUserId=user_id)
    friend_reqs = []
    for req in reqs:
        friend_reqs.append({'fromUserId': req.fromUserId, 'toUserId': req.toUserId, 'status': str(req.status)})
    return {'requests': friend_reqs}


def getAllUsersLocation():
    locations = db.session.query(Location).filter_by(isCycleService=False).all()
    json_locations = []
    for i in locations:
        json_locations.append(
            {'id': i.id, 'lat': i.lat, 'lng': i.lng, 'userId': i.userId, 'isCycleService': i.isCycleService})
    return {'locations': json_locations}


def getEcycleServices():
    locations = db.session.query(Location).filter_by(isCycleService=True).all()
    json_locations = []
    for i in locations:
        json_locations.append(
            {'id': i.id, 'lat': i.lat, 'lng': i.lng, 'userId': i.userId, 'isCycleService': i.isCycleService})
    return {'locations': json_locations}


def getCycleHistory(userId):
    routes = db.session.query(CycledRoute).all()
    json_routes = []
    for i in routes:
        json_routes.append(
            {'id': i.id, 'userId': i.userId, 'distanceTraveled': i.distanceTraveled, 'caloriesBurned': i.caloriesBurned,
             'route': i.route})
    return {'routes': json_routes}


def editPost(postBody):
    post = db.session.query(Post).get(postBody['id'])
    if post:
        if postBody['text']:
            post.text = postBody['text']
        if postBody['image']:
            post.image = postBody['image']
        db.session.commit()
        return True
    else:
        return {'error': 'Post not found'}, 404


def deletePost(postId):
    post = db.session.query(Post).filter_by(id=postId).one()
    db.session.query(Post).delete(post)
    db.session.commit()
    isPostPresent = db.session.query(Post).filter_by(id=postId).one()
    if isPostPresent:
        return False
    else:
        return True


def deleteCyclingParty(delPartyBody):
    creatorId = CycleParty.query.filter_by(id=delPartyBody['partyId']).first().partyCreatorId
    if delPartyBody['userId'] == creatorId:
        partyToDelete = CycleParty.query.filter_by(id=delPartyBody['partyId']).first()
        CyclePartyMember.query.filter_by(partyId=delPartyBody['partyId']).delete()
        db.session.delete(partyToDelete)
        db.session.commit()


def addCycledRoute(cycledRouteBody):
    # calculating the distance traveled
    # approximation of the radius of the earth in km
    R = 6373.0

    latFrom = math.radians(float(Route.query.filter_by(id=cycledRouteBody['route']).first().latFrom))
    lngFrom = math.radians(float(Route.query.filter_by(id=cycledRouteBody['route']).first().lngFrom))
    latTo = math.radians(float(Route.query.filter_by(id=cycledRouteBody['route']).first().latTo))
    lngTo = math.radians(float(Route.query.filter_by(id=cycledRouteBody['route']).first().lngTo))

    deltaLng = lngTo - lngFrom
    deltaLat = latFrom - latTo

    # using the haversine formula to determine the distance which the user traveled
    a = (math.sin(deltaLat / 2)) ** 2 + math.cos(latFrom) * math.cos(latTo) * (math.sin(deltaLng / 2)) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    # burned calories = ((MET * userWeight * 3.5) / 200) * cycledTime
    # where the MET values are provided by "The Compendium of Physical Activities 2011"
    MET = 1

    if distance <= 8.8:
        MET = 4
    elif distance >= 9 and distance <= 16:
        MET = 6.3
    elif distance >= 17 and distance < 24:
        MET = 7.4
    elif distance >= 24 and distance < 30:
        MET = 10
    else:
        MET = 20

    burnedCalories = ((MET * float(cycledRouteBody['userWeight']) * 3.5) / 200) * float(cycledRouteBody['cycledTime'])

    new_cycledRoute = CycledRoute(
        userId=cycledRouteBody['userId'],
        distanceTraveled=str(distance),
        userWeight=cycledRouteBody['userWeight'],
        cycledTime=float(cycledRouteBody['cycledTime']),
        caloriesBurned=burnedCalories,
        route=cycledRouteBody['route']
    )

    db.session.add(new_cycledRoute)
    db.session.commit()


def leaveParty(leavePartyBody):
    # TODO : If the party creator decides to leave the party then delete the entire party (I'll do it tmrw)
    partyToLeave = CyclePartyMember.query.filter_by(
        userId=leavePartyBody['userId'],
        partyId=leavePartyBody['partyId']
    ).first()
    db.session.delete(partyToLeave)

    # check if the party is now empty, if it is delete it from the db
    party = CyclePartyMember.query.filter_by(partyId=leavePartyBody['partyId']).first()
    if party is None:
        partyToDelete = CycleParty.query.filter_by(id=leavePartyBody['partyId']).first()
        db.session.delete(partyToDelete)

    db.session.commit()


def createPost(postBody):
    new_post = Post(
        userId=postBody['userId'],
        text=postBody['text'],
        createdOn=datetime.now())
    db.session.add(new_post)
    db.session.commit()


def postComment(commentBody):
    new_comment = Comment(
        postId=commentBody['postId'],
        userId=commentBody['userId'],
        text=commentBody['text'],
        createdOn=datetime.now()
    )
    db.session.add(new_comment)
    db.session.commit()


def addRoute(routeBody):
    new_route = Route(
        lngFrom=routeBody['lngFrom'],
        latFrom=routeBody['latFrom'],
        lngTo=routeBody['lngTo'],
        latTo=routeBody['latTo']
    )
    db.session.add(new_route)
    db.session.commit()


def createCycleParty(cyclePartyBody):
    new_cycleParty = CycleParty(
        route=cyclePartyBody['routeId'],
        partyCreatorId=cyclePartyBody['partyCreatorId'])
    db.session.add(new_cycleParty)

    db.session.commit()
    first_member = CyclePartyMember(
        partyId=CycleParty.query.filter_by(partyCreatorId=cyclePartyBody['partyCreatorId']).first().id,
        userId=cyclePartyBody['partyCreatorId'],
    )
    db.session.add(first_member)

    db.session.commit()


def sendMessage(msgBody):
    if msgBody['fromUserId'] != msgBody['toUserId']:
        d = datetime.now()
        new_message = Message(
            fromUserId=msgBody['fromUserId'],
            toUserId=msgBody['toUserId'],
            dateSent=d,
            text=msgBody['text'])
        db.session.add(new_message)
        db.session.commit()


def sendFriendRequest(friendRequestBody):
    if friendRequestBody['fromUserId'] != friendRequestBody['toUserId']:
        new_friendRequest = FriendRequest(
            fromUserId=friendRequestBody['fromUserId'],
            toUserId=friendRequestBody['toUserId'])
        db.session.add(new_friendRequest)
        db.session.commit()


def ackFriendRequest(friendBody):
    if friendBody['requestSender'] != friendBody['requestRecepient']:
        if friendBody['resp'] == True:
            new_friends = Friends(user1Id=friendBody['requestSender'], user2Id=friendBody['requestRecepient'])
            db.session.add(new_friends)
            FriendRequest.query.filter_by(fromUserId=friendBody['requestSender']).delete()
            db.session.commit()
        else:
            FriendRequest.query.filter_by(fromUserId=friendBody['requestSender']).delete()
            db.session.commit()


def getUserConversation(msgBody):
    messages = db.session.query(Message).filter_by(fromUserId=msgBody['fromUserId'],
                                                   toUserId=msgBody['toUserId'])
    json_messages = []
    for m in messages:
        json_messages.append({'fromUserId': m.fromUserId, 'toUserId': m.toUserId, 'text': m.text})
    return {'messages': json_messages}


def editCyclingParty(cyclePartyBody):
    cycleParty = db.session.query(CycleParty).get(cyclePartyBody['id'])
    if cycleParty:
        partyRoute = db.session.query(Route).get(cyclePartyBody['routeId'])
        if partyRoute:
            partyRoute.lngFrom = cycleParty["lngFrom"]
            partyRoute.latFrom = cycleParty["latFrom"]
            partyRoute.lngTo = cycleParty["lngTo"]
            partyRoute.latTo = cycleParty["latTo"]
            db.session.commit()
        return True
    else:
        return {'error': 'Cycle Party not found'}, 404


def editComment(commentBody):
    comment = db.session.query(Comment).get(commentBody['id'])
    if comment:
        if commentBody['text']:
            comment.text = commentBody['text']
        db.session.commit()
        return True
    else:
        return {'error': 'Comment not found'}, 404


def deleteComment(commentId):
    comment = db.session.query(Comment).filter_by(id=commentId).one()
    db.session.query(Comment).delete(comment)
    db.session.commit()
    isCommentPresent = db.session.query(Comment).filter_by(id=commentId).one()
    if isCommentPresent:
        return False
    else:
        return True


connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/social-db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

from models import *

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
