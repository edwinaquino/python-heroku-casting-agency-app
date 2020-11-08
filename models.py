# [OK] PYCODESTYLE COMPLETED
import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date
from settings import DATABASE_URL, APP_ENV

# ###################################################
# ############ START ACTORS ENDPOINTS ###############
# ###################################################

if APP_ENV == "remote":
    database_path = os.environ.get('HORUKO_DATABASE_URL')
else:
    database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename
    variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_init_records()


'''
Initialize records
'''


def db_init_records():
    new_actor = (Actor(name='John Travolta', gender='Male', age=45))
    new_movie = (Movie(title='Grease', release_date=date.today()))
    new_performance = Performance.insert().values(Movie_id=new_movie.id,
                                                  Actor_id=new_actor.id,
                                                  actor_fee=700.00)

    # PEFORM DATBASE ACTIONS
    new_actor.insert()
    new_movie.insert()
    db.session.execute(new_performance)
    db.session.commit()


Performance = db.Table(
    'Performance', db.Model.metadata,
    db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('Actor_id', db.Integer, db.ForeignKey('actors.id')),
    db.Column('actor_fee', db.Float))

# ###################################################
# ############  START ACTORS MODELS   ###############
# ###################################################


class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    favorite_color = Column(String)
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.favorite_color
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'favorite_color': self.favorite_color,
            'age': self.age
        }


# ###################################################
# ############  START MOVIES MODELS   ###############
# ###################################################


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    actors = db.relationship('Actor',
                             secondary=Performance,
                             backref=db.backref('performances', lazy='joined'))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
