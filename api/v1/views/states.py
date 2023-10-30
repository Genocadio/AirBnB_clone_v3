#!/usr/bin/python3
""" states object file """
from api.v1.views import app_views
from flask import jsonify, abort, request
from os import name


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """ get all states """
    from models import storage
    states = storage.all("State")
    states = [state.to_dict() for state in states.values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """ get a state """
    objects = storage.get('State', 'state_id')
    if objects is None:
        abort(404)
    return jsonify(objects.to_dict()), 'OK'

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """ delete a state """
    objects = storage.get('State', 'state_id')
    if objects is None:
        abort(404)
    storage.delete(objects)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def mkstate():
    """Creates a state"""
    response = request.get_json()
    if response id None:
        abort(400, {'Not a JSON'})
    if "name" not in response:
        abort(400, {'Missing name'})
    stateObject = State(name=response['name'])
    storage.new(stateObject)
    storage.save()
    return jsonify(stateObject.to_dict()), '201'


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update():
    """Updates a state"""
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    objects = storage.get('State', 'state_id')
    if objects is None:
        abort(404)
    for key, value in response.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(objects, key, value)
    storage.save()
    return jsonify(objects.to_dict()), '200'
