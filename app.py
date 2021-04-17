import connexion
from sqlalchemy import or_
from flask import jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json


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
    for post in user_feed:
        user_post_feed.append({'userId': post.userId, 'text': post.text, 'comments': post.comments})
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
    reqs = db.session.query(FriendRequest).filter(toUserId=user_id)
    friend_reqs = []
    for req in reqs:
        friend_reqs.append({'fromUserId': req.fromUserId, 'toUserId': req.toUserId, 'status': req.status})
    return {'requests': friend_reqs}


connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/social-db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

from models import *

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
