from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    favorite_planets = db.relationship('Fav_Planets', backref='user', lazy=True)
    favorite_people = db.relationship('Fav_People', backref='user', lazy=True)


    def __repr__(self):
        return '<user %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email

        }

class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
    
class People(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(120), unique=True)
    race = db.Column(db.String(120), unique=True)

    favorite_people = db.relationship('Fav_People', back_populates='people', lazy=True)

    def __repr__(self):
        return '<people %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "race": self.race

        }
    
class Fav_People(db.Model):
    __tablename__ = 'fav_People'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey ("user.id"))
    people_id = db.Column(db.Integer, db.ForeignKey ("people.id"))
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(120), unique=True)

    people = db.relationship('People', back_populates='favorite_people')

    def __repr__(self):
        return '<fav_People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id" : self.user_id,
            "people_id" : self.people_id,
            "name": self.name,
            "description": self.description,
        }

class Fav_Planets(db.Model):
    __tablename__ = 'fav_Planets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(120), unique=True)

    planet = db.relationship('Planet', backref='favorite_planets')

    def __repr__(self):
        return '<fav_Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "name": self.name,
            "description": self.description,
        }