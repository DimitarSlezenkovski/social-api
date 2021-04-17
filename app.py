import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
import math


def get_test1(test1_id):
    return {'id': 1, 'name': 'name', 'entered_id': test1_id}


def get_user_conversation(messageBody):
    messages = db.session.query(Message).filter_by(fromUserId=messageBody['fromUserId'], toUserId=messageBody['toUserId'])
    json_messages = []
    for m in messages:
        json_messages.append({'fromUserId': m.fromUserId, 'toUserId': m.toUserId, 'text': m.text})
    return {'messages': json_messages}


def edit_cycling_party(cyclePartyBody):
    cycleParty = db.session.query(CycleParty).get(cyclePartyBody['id'])
    if cycleParty:
        return True
    else:
        return {'error': 'Cycle Party not found'}, 404


def edit_comment(commentBody):
    comment = db.session.query(Comment).get(commentBody['id'])
    if comment:
        if commentBody['text']:
            comment.text = commentBody['text']
        db.session.commit()
        return True
    else:
        return {'error': 'Comment not found'}, 404


def delete_comment(commentId):
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/social-db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

from models import *

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
