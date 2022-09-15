# app.py

from flask_restx import Api, Resource
from config import app
from models import Movie
from schemas import MovieSchema

api = Api(app)
movies_ns = api.namespace('movies')
genres_ns = api.namespace('genres')
directors_ns = api.namespace('directors')


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies = Movie.query.all()
        result = MovieSchema(many=True).dump(movies)
        return result, 200

@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)
        result = MovieSchema(many=False).dump(movie)
        return result, 200

if __name__ == '__main__':
    app.run(debug=True)
