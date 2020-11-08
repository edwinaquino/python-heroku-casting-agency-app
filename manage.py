# [OK] PYCODESTYLE COMPLETED
from flask_script import Manager
from sqlalchemy import Column, String, Integer
from flask_migrate import Migrate, MigrateCommand
from models import db, Movie, Actor
from datetime import datetime
from app import create_app

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# INSERT SOME STARTING DATA USING THE FOLLOWING COMMANDS:
# $python3 manage.py db init
# $python3 manage.py db upgrade
# $python3 manage.py seed


@manager.command
def seed():
    Movie(title='When Harry Met Sally', release_date='1989-07-21').insert()
    Movie(title='The Shawshank Redemption', release_date='1994-09-22').insert()

    Actor(name='Meg Ryan', age=58, gender='female').insert()
    Actor(name='Tim Robbins', age=62, gender='male').insert()


if __name__ == '__main__':
    manager.run()
