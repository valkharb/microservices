import api

api.app.add_get('/my', api.password_editor.my)
api.app.add_post('/restore', api.password_editor.restore)
