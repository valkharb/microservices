import bson
import flask
import requests

import database.db_connector as connector


class UnauthorizedError(BaseException):
    pass


def base_response(text: str, code: int=200):
    return flask.Response(flask.escape(text), status=code)


def check_auth(db: connector.Database):
    args = flask.request.headers
    auth = args.get('Authorization', '')
    if not auth:
        raise UnauthorizedError('Unauthorized')
    token = auth.replace('Bearer ', '')
    if token == '':
        raise UnauthorizedError('Unauthorized')
    # TODO: create environment param for auth server
    user_id = requests.get(
        'https://localhost:8000',
        params={
            'token': token
        }
    )
    if user_id is None:
        raise UnauthorizedError('Unauthorized')
    user = db.users.findOne(
        {
            '_id': bson.ObjectId(user_id)
        }
    )
    if not user:
        raise UnauthorizedError('User not found')
    return user
