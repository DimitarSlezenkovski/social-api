import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json

def saveUserLocation(locationBody):
    new_location = Location(
        lng = locationBody['lng'],
        lat = locationBody['lat'],
        userId = locationBody['userId']
    )
    db.session.add(new_location)
    db.session.commit()
    return True

def getAllUsersLocation():
    locations = db.session.query(Location).filter_by(isCycleService=False).all()
    json_locations = []
    for i in locations
        json_locations.append({'id': i.id, 'lat': i.lat, 'lng': i.lng, 'userId': i.userId, 'isCycleService': i.isCycleService})
    return {'locations': json_locations}

def getEcycleServices():
    locations = db.session.query(Location).filter_by(isCycleService=True).all()
    json_locations = []
    for i in locations
        json_locations.append({'id': i.id, 'lat': i.lat, 'lng': i.lng, 'userId': i.userId, 'isCycleService': i.isCycleService})
    return {'locations': json_locations}

def getCycleHistory(userId)
    routes = db.session.query(CycledRoute).all()
    json_routes = []
    for i in routes
        json_routes.append({'id': i.id, 'userId': i.userId, 'distanceTraveled': i.distanceTraveled, 'caloriesBurned': i.caloriesBurned, 'route': i.route})
    return {'routes': json_routes}

def editPost(postBody):
    post = db.session.query(Post).get(postBody['id'])
    if post:
        if postBody['text']
            post.text = postBody['text']
        if postBody['image']
            post.image = postBody['image']
        db.session.commit()
        return True
    else:
        return {'error': 'Post not found'}, 404

def deletePost(postId)
    post = db.session.query(Post).filter_by(id=postId).one()
    db.session.query(Post).delete(post)
    db.session.commit()
    isPostPresent = db.session.query(Post).filter_by(id=postId).one()
    if isPostPresent:
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
