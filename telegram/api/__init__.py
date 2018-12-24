import flask

import database.db_connector as connector
import router_class


app = router_class.App(__name__)
app.config.from_envvar('MAIN_CONFIG')  # please, specify main config path


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


import api.telegram_client
import api.routes
