from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS  # to make response pretty
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_actors(): #check OK
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id(): #check OK
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()

    ### YOUR CODE HERE ###
    # use this for 200 response code
    if 'date_of_birth' in data.keys():
        try:
            date_upd=dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
        except:
            err = 'Wrong date of birth format!'
            return make_response(jsonify(error=err), 400)
    data_for_upd = dict(data)
    data_for_upd['date_of_birth'] = date_upd
    try:
        new_record = Actor.create(**data_for_upd)
    except:
        err = "Error occurred"
        return make_response(jsonify(error=err), 400)
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(new_actor), 200)
    ### END CODE HERE ###


def update_actor(): #check OK
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    for d in data.keys():
        if d not in ACTOR_FIELDS:
            err = 'Invalid fields'
            return make_response(jsonify(error=err), 400)
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        data_no_id = dict(data)
        del data_no_id['id']
        if 'date_of_birth' in data.keys():
            try:
                data_no_id['date_of_birth']=dt.strptime(data_no_id['date_of_birth'], '%d.%m.%Y').date()
            except:
                err = 'Invalid date of birth'
                return make_response(jsonify(error=err), 400)
        upd_record = Actor.update(row_id, **data_no_id)
        upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(upd_actor), 200)
    else:
        err = 'Id must be specified'
        return make_response(jsonify(error=err), 400)

    ### END CODE HERE ###


def delete_actor():  #check OK
    """
    Delete actor by id
    """
    '''data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        del_actor = Actor.delete(row_id)
        if del_actor==1:
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)'''

    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be an integer'
            return make_response(jsonify(error=err), 400)
        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'No movie with such id'
            return make_response(jsonify(error=err), 400)
        actor = Actor.delete(row_id)
        if actor > 0:
            msg = 'Actor successfully deleted!'
            return make_response(jsonify(message=msg), 200)
        else:
            err = 'Actor was not deleted'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'Id must be specified!'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def actor_add_relation(): #check OK
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' and 'relation_id' in data.keys():
        try:
            row_id = int(data['id'])
            rel_row_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Actor with such id does not exist'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        obj_movie = Movie.query.filter_by(id=rel_row_id).first()
        try:
            movie = {k: v for k, v in obj_movie.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Movie with such id does not exist'
            return make_response(jsonify(error=err), 400)
        actor = Actor.add_relation(row_id, obj_movie) # add relation here
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    else:
        err = 'Actor and movie Ids must be specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def actor_clear_relations(): #check OK
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
        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = "Actor with such id does not exist"
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        actor = Actor.clear_relations(row_id)# clear relations here
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    else:
        err = 'Id must be specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###