# [OK] PYCODESTYLE COMPLETED
import os
import json
import unittest
from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from app import create_app
# https://stackoverflow.com/questions/17273847/long-imports-in-python
from models import (setup_db, db_drop_and_create_all, Actor, Movie,
                    Performance, db_drop_and_create_all)
from settings import bearer_tokens, DATABASE_URL

from assertion_messages import assertions_message_arr

# ###################################################
# ############ 22 tests are included  ###############
# ###################################################

# ###################################################
# ############     AUTH0 TOKENS       ###############
# ###################################################

# GOT ERROR: TypeError: 'set' object is not subscriptable

assistant_token_header = {'Authorization': bearer_tokens['casting_assistant']}

directory_token_header = {'Authorization': bearer_tokens['casting_director']}

producer_token_header = {'Authorization': bearer_tokens['casting_producer']}

# ###################################################
# ############      Unittest Setup    ###############
# ###################################################


class CastingTestCase(unittest.TestCase):
    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = os.getenv('DATABASE_URL')
        setup_db(self.app, self.database_path)

        db_drop_and_create_all()

        # binds the app to the current context
        with self.app.app_context():

            self.db = SQLAlchemy()

            # initalizs db
            self.db.init_app(self.app)

            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

# ###################################################
# ADD NEW ACTOR
# ###################################################

    def test_create_new_actor(self):

        json_create_actor = {
            'name': 'John Mcwire',
            'gender': 'Male',
            'age': 46
        }

        res = self.client().post('/actors',
                                 json=json_create_actor,
                                 headers=directory_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)

    def test_401_new_actor(self):

        json_create_actor = {'name': 'Andrew', 'age': 23}

        res = self.client().post('/actors', json=json_create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'],
            assertions_message_arr['authorization_header_missing'])

    def test_422_create_new_actor(self):

        json_create_actor_without_name = {'age': 25}

        res = self.client().post('/actors',
                                 json=json_create_actor_without_name,
                                 headers=directory_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         assertions_message_arr['Unprocessable_entity'])

# ###################################################
# GET ACTORS
# ###################################################

    def test_get_all_actors(self):

        res = self.client().get('/actors?page=1',
                                headers=assistant_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_401_get_all_actors(self):

        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'],
            assertions_message_arr['authorization_header_missing'])

    def test_404_get_actors(self):

        res = self.client().get('/actors?page=1125125125',
                                headers=assistant_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         assertions_message_arr['not_found404'])

# ###################################################
# UPDATE ACTOR 1
# ###################################################

    def test_edit_movie(self):

        json_edit_movie = {'release_date': date.today()}
        res = self.client().patch('/movies/1',
                                  json=json_edit_movie,
                                  headers=producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)

    def test_400_edit_movie(self):

        res = self.client().patch('/movies/1', headers=producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         assertions_message_arr['invalid_body'])

    def test_404_edit_movie(self):

        json_edit_movie = {'release_date': date.today()}
        res = self.client().patch('/movies/99999',
                                  json=json_edit_movie,
                                  headers=producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         assertions_message_arr['movie_not_found'])

# ###################################################
# DELETE ACTOR
# ###################################################

    def test_401_delete_actor(self):

        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'],
            assertions_message_arr['authorization_header_missing'])

    def test_403_delete_actor(self):

        res = self.client().delete('/actors/1', headers=assistant_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         assertions_message_arr['permission_no_found_403'])

    def test_delete_actor(self):

        res = self.client().delete('/actors/1', headers=directory_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_404_delete_actor(self):

        res = self.client().delete('/actors/99999',
                                   headers=directory_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         assertions_message_arr['not_found404'])

# ###################################################
# ADD MOVIE
# ###################################################

    def test_create_new_movie(self):

        json_create_movie = {
            'title': 'Fullstack Developer Movie',
            'release_date': date.today()
        }

        res = self.client().post('/movies',
                                 json=json_create_movie,
                                 headers=producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)

    def test_422_create_new_movie(self):

        json_create_movie_without_name = {'release_date': date.today()}

        res = self.client().post('/movies',
                                 json=json_create_movie_without_name,
                                 headers=producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Unprocessable entity')

# ###################################################
# ADD MOVIES
# ###################################################

    def test_get_all_movies(self):

        res = self.client().get('/movies?page=1',
                                headers=assistant_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_401_get_all_movies(self):

        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'],
            assertions_message_arr['authorization_header_missing'])

    def test_404_get_movies(self):

        res = self.client().get('/movies?page=99999999',
                                headers=assistant_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         assertions_message_arr['not_found404'])

# ###################################################
# PATCH MOVIE
# ###################################################

    def test_edit_movie(self):

        json_edit_movie = {'release_date': date.today()}
        res = self.client().patch('/movies/1',
                                  json=json_edit_movie,
                                  headers=producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)

    def test_400_edit_movie(self):

        res = self.client().patch('/movies/1', headers=producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad Request')

    def test_404_edit_movie(self):

        json_edit_movie = {'release_date': date.today()}
        res = self.client().patch('/movies/99999',
                                  json=json_edit_movie,
                                  headers=producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         assertions_message_arr['not_found404'])

# ###################################################
# DELETE MOVIE
# ###################################################

    def test_401_delete_movie(self):

        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'],
            assertions_message_arr['authorization_header_missing'])

    def test_403_delete_movie(self):

        res = self.client().delete('/movies/1', headers=assistant_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         assertions_message_arr['permission_no_found_403'])

    def test_delete_movie(self):

        res = self.client().delete('/movies/1', headers=producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_404_delete_movie(self):

        res = self.client().delete('/movies/151251',
                                   headers=producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         assertions_message_arr['not_found404'])


# ###################################################
# RUN UNITTEST
# ###################################################

if __name__ == "__main__":
    unittest.main()
