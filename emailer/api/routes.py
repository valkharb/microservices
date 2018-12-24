import api


api.app.add_get('/my', api.email_client.my)
api.app.add_post('/send', api.email_client.send)
