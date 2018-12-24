import random
import string
import passlib.hash

import flask
import pymongo

import api
import base_helper
import emailer.helper


DEFAULT_SENDER = 'help@microservices.ru'


def password_generator():
    pass_len = random.randint(8, 24)
    return ''.join(
        [
            random.choice(
                string.ascii_lowercase
            ) for _ in range(pass_len)
        ]
    )


def my():
    message_pattern = (
        'Your login: {} \n '
        '{} \n {} \n {} \n '
        'Your role at our service is {}.'
    )
    user = base_helper.check_auth(api.db)
    login = user.get('login')
    if not login:
        return base_helper.base_response('Can not authenticate you.', 401)

    fullname = user.get('fullname')
    fullname_msg = (
        'You introduced yourself as {}'.format(fullname)
        if fullname is not None else 'You did not introduced yourself.')
    email = user.get('email')
    email_msg = (
        'Your notifications are sent at {}'.format(email)
        if email is not None else 'You did not provide an email.')
    telegram = user.get('nickname')
    telegram_msg = (
        'Our bot knows you as {}'.format(telegram)
        if telegram is not None else 'You have no telegram yet...')
    role = user.get('role', 'user')

    message = message_pattern.format(login, fullname_msg, email_msg,
                                     telegram_msg, role)

    return base_helper.base_response(message)


def restore():
    user = base_helper.check_auth(api.db)
    login = user.get('login')

    if not login:
        return base_helper.base_response('Can not authenticate you.', 401)

    args = flask.request.get_json()
    code_word = args.get('code_word')
    email = args.get('email')
    if not code_word:
        return base_helper.base_response('Please provide the code word!', 400)

    if not passlib.hash.pbkdf2_sha256.verify(code_word, user.get('code_word')):
        return base_helper.base_response('Your code word is incorrect, try again.', 403)

    randomword = password_generator()
    new_pwd = passlib.hash.pbkdf2_sha256.hash(randomword)
    user_email = user.get('email')
    if email or user_email:
        email = email if email else user_email
        try:
            api.db.users.find_one_and_update(
                {
                    'login': 'login'
                },
                {
                    '$set': {
                        'password': new_pwd
                    }
                }
            )
        except pymongo.errors.WriteError:
            return base_helper.base_response('Something went wrong while connecting to '
                            'database. Try again later.', 500)
        return emailer.helper.email_sender(None, api.app,
                                           subject='Your new password',
                                           body=randomword,
                                           sender=DEFAULT_SENDER,
                                           recipients=[email])
    else:
        return base_helper.base_response(
            'Cannot change your password. '
            'We need your email for password recovery.', 403)
