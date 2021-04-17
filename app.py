import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
import math

def deleteComment(delCommentBody):
    return

def deleteCyclingParty(delPartyBody):
    creatorId = CycleParty.query.filter_by(id = delPartyBody['partyId']).first().partyCreatorId
    if delPartyBody['userId'] == creatorId :
        partyToDelete = CycleParty.query.filter_by(id = delPartyBody['partyId']).first()
        CyclePartyMember.query.filter_by(partyId=delPartyBody['partyId']).delete()
        db.session.delete(partyToDelete)
        db.session.commit()

def addCycledRoute(cycledRouteBody):
    # calculating the distance traveled
    # approximation of the radius of the earth in km
    R = 6373.0

    latFrom = math.radians(float(Route.query.filter_by(id = cycledRouteBody['route']).first().latFrom))
    lngFrom = math.radians(float(Route.query.filter_by(id = cycledRouteBody['route']).first().lngFrom))
    latTo = math.radians(float(Route.query.filter_by(id = cycledRouteBody['route']).first().latTo))
    lngTo = math.radians(float(Route.query.filter_by(id = cycledRouteBody['route']).first().lngTo))
    
    deltaLng = lngTo - lngFrom
    deltaLat = latFrom - latTo

    # using the haversine formula to determine the distance which the user traveled
    a = (math.sin(deltaLat/2))**2 + math.cos(latFrom) * math.cos(latTo) * (math.sin(deltaLng/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c

    # burned calories = ((MET * userWeight * 3.5) / 200) * cycledTime 
    # where the MET values are provided by "The Compendium of Physical Activities 2011" 
    MET = 1
    
    if distance <= 8.8:
        MET = 4
    elif distance >= 9 and distance <= 16 : 
        MET = 6.3
    elif distance >= 17 and distance < 24 :
        MET = 7.4
    elif distance >= 24 and distance < 30 :
        MET = 10
    else : 
        MET = 20

    burnedCalories = ((MET * float(cycledRouteBody['userWeight']) * 3.5) / 200) * float(cycledRouteBody['cycledTime'])

    new_cycledRoute = CycledRoute(
        userId = cycledRouteBody['userId'],
        distanceTraveled = str(distance),
        userWeight = cycledRouteBody['userWeight'],
        cycledTime = float(cycledRouteBody['cycledTime']),
        caloriesBurned = burnedCalories,
        route = cycledRouteBody['route']
    )

    db.session.add(new_cycledRoute)
    db.session.commit()

def leaveParty(leavePartyBody):
    #TODO : If the party creator decides to leave the party then delete the entire party (I'll do it tmrw)
    partyToLeave = CyclePartyMember.query.filter_by(
        userId = leavePartyBody['userId'],
        partyId = leavePartyBody['partyId']
        ).first()
    db.session.delete(partyToLeave)
    
    #check if the party is now empty, if it is delete it from the db
    party = CyclePartyMember.query.filter_by(partyId = leavePartyBody['partyId']).first()
    if party is None:
        partyToDelete = CycleParty.query.filter_by(id = leavePartyBody['partyId']).first()
        db.session.delete(partyToDelete)

    db.session.commit()

def createPost(postBody):
    new_post = Post(
        userId = postBody['userId'], 
        text = postBody['text'], 
        createdOn = datetime.now())
    db.session.add(new_post)
    db.session.commit()

def postComment(commentBody):
    new_comment = Comment(
        postId = commentBody['postId'],
        userId = commentBody['userId'],
        text = commentBody['text'],
        createdOn = datetime.now()
    )
    db.session.add(new_comment)
    db.session.commit()

def addRoute(routeBody):
    new_route = Route(
        lngFrom = routeBody['lngFrom'],
        latFrom = routeBody['latFrom'],
        lngTo = routeBody['lngTo'],
        latTo = routeBody['latTo']
        )
    db.session.add(new_route)
    db.session.commit()

def createCycleParty(cyclePartyBody):
    new_cycleParty = CycleParty(
        route = cyclePartyBody['routeId'], 
        partyCreatorId = cyclePartyBody['partyCreatorId'])
    db.session.add(new_cycleParty)

    db.session.commit()
    first_member = CyclePartyMember(
        partyId = CycleParty.query.filter_by(partyCreatorId=cyclePartyBody['partyCreatorId']).first().id,
        userId = cyclePartyBody['partyCreatorId'],
    )
    db.session.add(first_member)

    db.session.commit()

def sendMessage(msgBody):
    if friendRequestBody['fromUserId'] != friendRequestBody['toUserId'] :
        d = datetime.now()
        new_message = Message(
            fromUserId=msgBody['fromUserId'], 
            toUserId=msgBody['toUserId'], 
            dateSent=d, 
            text=msgBody['text'])
        db.session.add(new_message)
        db.session.commit()

def sendFriendRequest(friendRequestBody):
    if friendRequestBody['fromUserId'] != friendRequestBody['toUserId'] :
        new_friendRequest = FriendRequest(
            fromUserId = friendRequestBody['fromUserId'],
            toUserId = friendRequestBody['toUserId'])
        db.session.add(new_friendRequest)
        db.session.commit()

def ackFriendRequest(friendBody):
    if friendBody['requestSender'] != friendBody['requestRecepient'] :
        if friendBody['resp'] == True:
            new_friends = Friends(user1Id = friendBody['requestSender'], user2Id = friendBody['requestRecepient'])
            db.session.add(new_friends)
            FriendRequest.query.filter_by(fromUserId = friendBody['requestSender']).delete()
            db.session.commit()
        else :
            FriendRequest.query.filter_by(fromUserId = friendBody['requestSender']).delete()
            db.session.commit()

connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/social-db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

from models import *

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
