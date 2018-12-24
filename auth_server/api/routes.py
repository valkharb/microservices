import api

api.app.add_get('/endpoint', api.handlers.restricted_access)

api.app.add_get('/check_auth', api.handlers.BearerAuth)
