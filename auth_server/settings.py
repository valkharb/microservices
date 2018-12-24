RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']
users = {
    'item_title': 'person',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'lastname'
    },
    'schema': {
        'login': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 20,
            'required': True,
            'unique': True,
        },
        'fullname': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 50,
            },
        'role': {
            'type': 'list',
            'allowed': ["admin", "user"],
        },
        'email': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 40,
            'unique': True,
        },
        'nickname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 20,
            'required': True,
            'unique': True,
        },
        'code_word': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 20,
            'required': True,
            'unique': True,
        },
    }
}

works = {
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'schema': {
        'title': {
            'type': 'string',
            'required': True,
        },
        'description': {
            'type': 'string',
        },
        'owner': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'people',
                'embeddable': True
            },
        },
    }
}

DOMAIN = {
    'users': users
}