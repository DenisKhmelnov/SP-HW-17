# app.py
from flask import request
from flask_restx import Api, Resource
from config import app, db
from models import Movie, Director, Genre
from schemas import MovieSchema, DirectorSchema, GenreSchema

api = Api(app)
movies_ns = api.namespace('movies')
genres_ns = api.namespace('genres')
directors_ns = api.namespace('directors')


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        try:
            director_id = request.args.get('director_id')
            genre_id = request.args.get('genre_id')
            query = Movie.query
            if director_id:
                query = query.filter(Movie.director_id == director_id)
            if genre_id:
                query = query.filter(Movie.genre_id == genre_id)
            movies = query.all()
            result = MovieSchema(many=True).dump(movies)
            return result, 200
        except Exception as e:
            return e, 500

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        db.session.add(new_movie)
        db.session.commit()
        return "", 201

@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        try:
            movie = Movie.query.get(mid)
            result = MovieSchema(many=False).dump(movie)
            return result, 200
        except Exception as e:
            return e, 500

    def put(self, mid):
        req_json = request.json
        movie = Movie.query.get(mid)
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, mid):
        movie = Movie.query.get(mid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204

@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        try:
            direcors = Director.query.all()
            result = DirectorSchema(many=True).dump(direcors)
            return result, 200
        except Exception as e:
            return e, 500

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        db.session.add(new_director)
        db.session.commit()
        return "", 201

@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        try:
            director = Director.query.get(did)
            result = DirectorSchema(many=False).dump(director)
            return result, 200
        except Exception as e:
            return e, 500

    def put(self, did):
        req_json = request.json
        director = Director.query.get(did)
        director.name = req_json["name"]
        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, did):
        director = Director.query.get(did)
        db.session.delete(director)
        db.session.commit()
        return "", 204

@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        try:
            genres = Genre.query.all()
            result = GenreSchema(many=True).dump(genres)
            return result, 200
        except Exception as e:
            return e, 500

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        db.session.add(new_genre)
        db.session.commit()
        return "", 201

@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        try:
            genre = Genre.query.get(gid)
            result = GenreSchema(many=False).dump(genre)
            return result, 200
        except Exception as e:
            return e, 500

    def put(self, gid):
        req_json = request.json
        genre = Genre.query.get(gid)
        genre.name = req_json["name"]
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, gid):
        genre = Genre.query.get(gid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
