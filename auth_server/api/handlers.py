import flask
import flask_sentinel
import redis

import api
import base_helper


@flask_sentinel.oauth.require_oauth()
def restricted_access():
    return True


class BearerAuth(object):

    def __init__(self):
        self.mongo = api.db
        self.redis = redis.StrictRedis()
        self.redis.connection_pool = redis.ConnectionPool.from_url(
            api.app.config['REDIS_URL']
        )

    def get(self):
        token = flask.request.args.get('token', '')
        return base_helper.base_response(
            str(self.check_auth(token))
        )

    def set_mongo_prefix(self, value):
        flask.g.mongo_prefix = value

    def get_mongo_prefix(self):
        return flask.g.get("mongo_prefix")

    def set_request_auth_value(self, value):
        flask.g.auth_value = value

    def get_request_auth_value(self):
        return flask.g.get("auth_value")

    def get_user_or_token(self):
        return flask.g.get("user")

    def set_user_or_token(self, user):
        flask.g.user = user

    def authenticate(self):
        resp = base_helper.base_response('Unauthorized', 401)
        flask.abort(
            401,
            description="Please provide proper credentials",
            response=resp)

    def check_auth(self, token, allowed_roles=None,
                   resource=None, method=None):
        return token and self.redis.get(token)

    def authorized(self, allowed_roles, resource, method):
        try:
            token = flask.request.headers.get('Authorization').split(' ')[1]
        except BaseException:
            token = None
        return self.check_auth(token, allowed_roles, resource, method)
