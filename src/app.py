"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import Planet, db, User, People, Fav_People, Fav_Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_get_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))
    

    return jsonify(all_users), 200

@app.route('/user/<int:id>', methods=['GET'])
def handle_get_user(id):
    user = User.query.get(id)
    user = user.serialize()

    return jsonify(user), 200

@app.route('/user', methods=['POST'])
def handle_add_user():
    body = request.get_json()
    if 'name' not in body:
        return jsonify({'msg': 'error name empty'}), 400
    if 'email' not in body:
        return jsonify({'msg': 'error email empty'}), 400
    if 'password' not in body:
        return jsonify({'msg': 'error password empty'}), 400
    
    new_user = User();
    new_user.name = body['name']
    new_user.email = body['email']
    new_user.password = body['password']  

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@app.route('/user/<int:id>', methods=['DELETE'])
def handle_delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'msg' : 'id not exist'})
    db.session.delete(user)
    db.session.commit()

    return jsonify({}), 204


@app.route('/planet', methods=['GET'])
def handle_get_planets():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    

    return jsonify(all_planets), 200


@app.route('/planet/<int:id>', methods=['GET'])
def handle_get_planet(id):
    planet = Planet.query.get(id)
    planet = planet.serialize()

    return jsonify(planet), 200


@app.route('/planet', methods=['POST'])
def handle_add_planet():
    body = request.get_json()
    if 'name' not in body:
        return jsonify({'msg': 'error name empty'}), 400
    if 'description' not in body:
        return jsonify({'msg': 'error description empty'}), 400
    if 'population' not in body:
        return jsonify({'msg': 'error population empty'}), 400
    
    
    new_planet = Planet();
    new_planet.name = body['name']
    new_planet.description = body['description'] 
    new_planet.population = body['population']


    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 201


@app.route('/planet/<int:id>', methods=['DELETE'])
def handle_delete_planet(id):
    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({'msg' : 'id not exist'})
    db.session.delete(planet)
    db.session.commit()

    return jsonify({}), 204


@app.route('/people', methods=['GET'])
def handle_get_peoples():
    all_peoples = People.query.all()
    all_peoples = list(map(lambda x: x.serialize(), all_peoples))
    

    return jsonify(all_peoples), 200


@app.route('/people/<int:id>', methods=['GET'])
def handle_get_people(id):
    people = People.query.get(id)
    people = people.serialize()

    return jsonify(people), 200


@app.route('/people', methods=['POST'])
def handle_add_people():
    body = request.get_json()
    if 'name' not in body:
        return jsonify({'msg': 'error name empty'}), 400
    if 'description' not in body:
        return jsonify({'msg': 'error description empty'}), 400
    if 'race' not in body:
        return jsonify({'msg': 'error race empty'}), 400
    
    
    new_people = People();
    new_people.name = body['name']
    new_people.description = body['description'] 
    new_people.race = body['race']


    db.session.add(new_people)
    db.session.commit()

    return jsonify(new_people.serialize()), 201


@app.route('/people/<int:id>', methods=['DELETE'])
def handle_delete_people(id):
    people = People.query.get(id)
    if people is None:
        return jsonify({'msg' : 'id not exist'})
    db.session.delete(people)
    db.session.commit()

    return jsonify({}), 204

@app.route('/user/favs', methods=['GET'])
def get_user_favs():
    data = request.get_json()
    user_id = data.get('user_id')

    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    favs = {
        "favorite_planets": [{"id": fav.planet_id, "name": fav.planet.name} for fav in user.favorite_planets],
        "favorite_people": [{"id": fav.people_id, "name": fav.people.name} for fav in user.favorite_people]
    }

    return jsonify(favs), 200

@app.route('/fav/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    data = request.get_json()
    user_id = data.get('user_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    fav = Fav_Planets(user_id=user_id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()

    return jsonify({"message": "Favorite planet added"}), 201

@app.route('/fav/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
    data = request.get_json()
    user_id = data.get('user_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error" : "User not found"}), 404

    fav = Fav_People(user_id=user_id, people_id=people_id)
    db.session.add(fav)
    db.session.commit()

    return jsonify({"message" : "Fav person added"}), 201


@app.route('/fav/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people(people_id):
    data = request.get_json()
    user_id = data.get('user_id')

    fav = Fav_People.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not fav:
        return jsonify({"error" : "Fav person not found"}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"message" : "Fav person deleted"}), 200

@app.route('/fav/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    data = request.get_json()
    user_id = data.get('user_id')

    fav = Fav_Planets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"error" : "Fav planet not found"}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"message" : "Fav planet deleted"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
