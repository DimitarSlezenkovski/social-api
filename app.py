import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime

def sendMessage(msgBody): 
    d = datetime.now()
    new_message = Message(
        fromUserId=msgBody['fromUserId'], 
        toUserId=msgBody['toUserId'], 
        dateSent=d, 
        text=msgBody['text'])
    db.session.add(new_message)
    db.session.commit()

def sendFriendRequest(friendRequestBody):
    new_friendRequest = FriendRequest(
        fromUserId = friendRequestBody['fromUserId'],
        toUserId = friendRequestBody['toUserId'])
    db.session.add(new_friendRequest)
    db.session.commit()

def ackFriendRequest(friendBody):


connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/social-db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

from models import *

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
