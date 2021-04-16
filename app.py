import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime

def addRoute(routeBody):
    new_route = Route(
        lng = routeBody['lng'],
        lat = routeBody['lat'])
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
            # TODO : DELETE FRIEND REQUEST FROM DB WHEN A FRIEND HAS BEEN ACCEPTED/REJECTED
            db.session.commit()
        #TODO : ADD AN ELSE PART WHERE YOU JUST REMOVE THE FRIEND REQUEST FROM THE DB

connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/social-db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

from models import *

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
