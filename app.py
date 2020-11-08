# [OK] PYCODESTYLE COMPLETED
import os
from flask import Flask, request, render_template, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db_drop_and_create_all, setup_db, Actor, Movie, Performance
from settings import APP_ENV, DOMAIN_NAME
from auth import AuthError, requires_auth, AUTH0_DOMAIN, API_AUDIENCE
from assertion_messages import assertions_message_arr

# Variables found in .env file
client_id = os.environ.get('AUTH0_APP_CLIENT_ID')

if APP_ENV == "remote":
    # HEROKU
    redirect_uri = os.environ.get('AUTH0_ALLOWED_CALLBACK_URL_HEROKU')
    DATABASE_URL = os.environ.get('HORUKO_DATABASE_URL')
else:
    # localhost
    redirect_uri = os.environ.get('AUTH0_ALLOWED_CALLBACK_URL')
    DATABASE_URL = os.environ.get('DATABASE_URL')

RESULTS_PER_PAGE = 10


# Code found from Project #3
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        """Set Access Control."""
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # get the page number call, then slice and format the returned results
    def format_pagination(call, choice):
        page_number = call.args.get('page', 1, type=int)
        page_start = (page_number - 1) * RESULTS_PER_PAGE
        page_end = page_start + RESULTS_PER_PAGE
        objects_formatted = [object_name.format() for object_name in choice]
        return objects_formatted[page_start:page_end]


# ###################################################
# ############ START ACTORS ENDPOINTS ###############
# ###################################################
# GET actors list

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        # def get_actors():
        actors = Actor.query.all()
        total_selected_actors = format_pagination(request, actors)
        # check if any actors exist in the database
        if len(total_selected_actors) == 0:
            abort(404, {'message': 'Actor not found.'})
        # resturn results in JSON
        return jsonify({'success': True, 'actors': total_selected_actors})

    # FOR DEUBUGGIN ONLY
    # NO AUTHENTICATION REQUIRED FOR THIS ENDPOINT.
    # THIS ENDPOINT IS TO TEST CONNECTION TO DATABASE IS WORKING
    @app.route('/actors/<actor_id>', methods=['GET'])
    def get_actor(actor_id):

        # ABORT IF MISSING PARAMETERS
        if not actor_id:
            abort(400, {'message': 'No actor_idwas provided'})
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(404, {'message': 'Actor was not found'.format(actor_id)})

        # RETURN RESULTS
        return jsonify({'success': True, 'actor': [actor.format()]})

    # create actor in list
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        # def create_actor():
        data = request.get_json()
        # CHECK IF THERE IS DATA
        if not data:
            abort(400, {'message': 'invalid JSON data.'})
        # assign variables from data object
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', 'Other')
        # validate parameters
        if not name:
            abort(422, {'message': 'Error: Missing name.'})
        if not age:
            abort(422, {'message': 'Error: Missing age.'})

        new_actor = Actor(name=name, age=age, gender=gender)
        new_actor.insert()
        # Return Results
        return jsonify({'success': True, 'created': new_actor.id})

    # Update an actor
    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, actor_id):
        # def update_actor(actor_id):
        data = request.get_json()
        selected_actor_id = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        # CHECK IF THERE IS DATA
        if not actor_id:
            abort(404, {'message': 'Actor was not provided.'})
        if not data:
            abort(400, {'message': 'Invalid JSON data.'})
        if not selected_actor_id:
            abort(404, {'message': 'Actor was not found'.format(actor_id)})

        # ASSING VARIABLES FROM DATA
        name = data.get('name', selected_actor_id.name)
        age = data.get('age', selected_actor_id.age)
        gender = data.get('gender', selected_actor_id.gender)

        # SET NEW VARIABLES.
        selected_actor_id.name = name
        selected_actor_id.age = age
        selected_actor_id.gender = gender

        # UPDATE DATBASE
        selected_actor_id.update()

        # RETURN RESULTS
        return jsonify({
            'success': True,
            'updated': selected_actor_id.id,
            'actor': [selected_actor_id.format()]
        })

    # Remove actor from database
    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        # def delete_actor(actor_id):

        # FILTER ACTOR IN DATABASE
        actor_to_delete = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        # CHECK FOR ANY ERRORS
        if not actor_id:
            abort(400, {'message': 'actor_id is not provided in end point'})

        if not actor_to_delete:
            abort(404, {'message': 'Actor was not found.'})

        # REMOVE ACTOR ID FROM DATABASE
        actor_to_delete.delete()

        # RETURN RESULTS
        return jsonify({'success': True, 'deleted': actor_id})

    # ###################################################
    # ############ START MOVIES ENDPOINTS ###############
    # ###################################################

    # Get all movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        # def get_movies():
        movies = Movie.query.all()
        movies_pagination = format_pagination(request, movies)
        # CHECK IF ANY MOVIES FOUND IN DATBASE
        if len(movies_pagination) == 0:
            abort(404, {'message': 'No movies found.'})
        # RETURN RESULTS
        return jsonify({'success': True, 'movies': movies_pagination})

    # FOR DEUBUGGIN ONLY
    # NO AUTHENTICATION REQUIRED FOR THIS ENDPOINT.
    # THIS ENDPOINT IS TO TEST CONNECTION TO DATABASE IS WORKING
    @app.route('/movies/<movie_id>', methods=['GET'])
    def get_movie(movie_id):

        # ABORT IF MISSING PARAMETERS
        if not movie_id:
            abort(400, {'message': 'No movie id was provided'})
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not movie:
            abort(404, {'message': 'Movie was not found'.format(movie_id)})

        # RETURN RESULTS
        return jsonify({
            'success': True,
            'edited': movie.id,
            'movie': [movie.format()]
        })

    # create new movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        # def create_movie():
        data = request.get_json()
        # CHECK POST DATA
        if not data:
            abort(400, {'message': 'Inalid JSON data.'})

        movie_title = data.get('title', None)
        release_date = data.get('release_date', None)

        # ABORT IF MISSING PARAMETERS
        if not movie_title:
            abort(422, {'message': 'No movie title was provided.'})
        if not release_date:
            abort(422, {'message': 'No movie relase date was provided.'})

        # CREATE MOVIE IN DATBASE
        movie = (Movie(title=movie_title, release_date=release_date))
        movie.insert()

        return jsonify({'success': True, 'created': movie.id})

    # UPDATE MOVIE
    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):
        # def update_movie(movie_id):
        data = request.get_json()

        # ABORT IF MISSING PARAMETERS
        if not movie_id:
            abort(400, {'message': 'No movie id was provided'})
        if not data:
            abort(400, {'message': 'Invalid JSON data.'})
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not movie:
            abort(404, {'message': 'Movie was not found'.format(movie_id)})

        title = data.get('title', movie.title)
        release_date = data.get('release_date', movie.release_date)
        movie.title = title
        movie.release_date = release_date

        # UPDATE DABASE
        movie.update()
        # RETURN RESULTS
        return jsonify({
            'success': True,
            'edited': movie.id,
            'movie': [movie.format()]
        })

    # DELETE A MOVIE
    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        # def delete_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        # ABORT IF MISSING PARAMETERS
        if not movie_id:
            abort(400, {'message': 'movie id was not provided'})
        if not movie:
            abort(404, {'message': 'Movie was not found.'})

        # DELETE MOVIE
        movie.delete()

        # RETURN RESULTS
        return jsonify({'success': True, 'deleted': movie_id})

    # TOOL FOR RECEIVING TOKEN FROM AUTHO AS THE RETURNED URL
    @app.route('/token', methods=['GET'])
    def token():
        return render_template('token.html',
                               AUTH0_DOMAIN=AUTH0_DOMAIN,
                               API_AUDIENCE=API_AUDIENCE,
                               client_id=client_id,
                               redirect_uri=redirect_uri)

    # TOOL FOR GENERATING AUTH0 TOKEN URL
    @app.route('/login', methods=['GET'])
    def login():
        return render_template('login.html',
                               DOMAIN_NAME=DOMAIN_NAME,
                               APP_ENV=APP_ENV,
                               DATABASE_URL=DATABASE_URL,
                               AUTH0_DOMAIN=AUTH0_DOMAIN,
                               API_AUDIENCE=API_AUDIENCE,
                               client_id=client_id,
                               redirect_uri=redirect_uri)

    # ###################################################
    # ############    Error Handlers      ###############
    # ###################################################
    # Common Codes
    #     200: OK
    #     201: Created
    #     304: Not Modified
    #     400: Bad Request
    #     401: Unauthorized
    #     404: Not Found
    #     422: Unprocessable entity
    #     405: Method Not Allowed
    #     500: Internal Server Error

    # 400: Bad Request
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    # 404: Not Found
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': assertions_message_arr['not_found404']
        }), 404

    # 422: Unprocessable entity
    @app.errorhandler(422)
    def unprocesable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    # 500: Internal Server Error
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error['description']
        }), AuthError.status_code

    # return after going through create_app() function
    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
