import api


api.app.add_get('/my', api.telegram_client.my)
api.app.add_post('/send', api.telegram_client.send)
