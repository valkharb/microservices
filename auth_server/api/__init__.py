import flask
import flask_sentinel
import redis

import database.db_connector as connector
import router_class


app = router_class.App(__name__)
app.config.from_object('settings')
app.config['MONGO_URI'] = connector.generate_mongo_connection_string()
app.config['REDIS_URL'] = connector.generate_redis_connection_string()
red = redis.Redis(app)


def get_db():
    if 'db' not in flask.g:
        flask.g.db = connector.connect()
    return flask.g.db


@app.teardown_appcontext
def teardown_db(self):
    db = flask.g.pop('db', None)

    if db is not None:
        db.client.close()


with app.app_context():
    db = get_db()


@flask_sentinel.oauth.require_oauth()
def restricted_access():
    return "You made it through and accessed the protected resource!"


flask_sentinel.ResourceOwnerPasswordCredentials(app)

import api.handlers
import api.routes
