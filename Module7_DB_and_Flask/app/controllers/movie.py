from flask import jsonify, make_response

from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS  # to make response pretty
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data

def get_all_movies():  #check OK
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return make_response(jsonify(movies), 200)

def get_movie_by_id(): #check OK
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be an integer'
            return make_response(jsonify(error = err), 400)
        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = "Record with such id does not exist"
            return make_response(jsonify(error=err), 400)
        return make_response(jsonify(movie), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

def add_movie(): #check OK
    data = get_request_data()
    try:
        movie = Movie.create(**data)
    except:
        err = 'Movie with such name already exists!'
        return make_response(jsonify(error=err), 400)
    new_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(new_movie), 200)

def update_movie():    #check OK
    # update movie record by id
    data = get_request_data()
    for d in data.keys():
        if d not in MOVIE_FIELDS:
            err = 'Invalid fields'
            return make_response(jsonify(error=err), 400)
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = "Id must be an integer"
            return make_response(jsonify(error=err), 400)
        if 'year' in data.keys():
            try:
                year_int = int(data['year'])
            except:
                err = 'Year must be integer'
                return make_response(jsonify(error=err), 400)
        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'No movie with such id'
            return make_response(jsonify(error=err), 400)
        data_no_id = dict(data)
        del data_no_id['id']
        data_no_id['year'] = year_int
        movie = Movie.update(row_id, **data_no_id)
        upd_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(upd_movie), 200)
    else:
        err = "Id must be specified"
        return make_response(jsonify(error=err), 400)

def delete_movie():     #check OK
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be an integer'
            return make_response(jsonify(error=err), 400)
        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'No movie with such id'
            return make_response(jsonify(error=err), 400)
        movie = Movie.delete(row_id)
        if movie >0:
            msg = 'Movie successfully deleted!'
            return make_response(jsonify(message=msg), 200)
        else:
            err = 'Movie was not deleted'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'Id must be specified!'
        return make_response(jsonify(error=err), 400)

def movie_add_relation():   #check OK
    data = get_request_data()
    if 'id' and 'relation_id' in data.keys():
        try:
            row_id = int(data['id'])
            rel_row_id = int(data['relation_id'])
        except:
            err = 'Id must be an integer'
            return make_response(jsonify(error=err), 400)
        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'No movie with such id'
            return make_response(jsonify(error=err), 400)
        actor = Actor.query.filter_by(id=rel_row_id).first()
        try:
            actor2 = {k: v for k, v in actor.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'No actor with such id'
            return make_response(jsonify(error=err), 400)
        movie = Movie.add_relation(row_id, actor)
        movie_add_rel = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movie_add_rel['cast'] = str(movie.cast)
        return make_response(jsonify(movie_add_rel), 200)
    else:
        err = 'Movie and actor Ids must be specified'
        return make_response(jsonify(error = err), 400)


def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'ID must be integer'
            return make_response(jsonify(err), 400)
        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = "Movie with such id does not exist"
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        movie = Movie.clear_relations(row_id)# clear relations here
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    else:
        err = 'Id must be specified'
        return make_response(jsonify(error=err), 400)




