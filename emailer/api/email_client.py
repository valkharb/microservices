import flask

import api
import base_helper
import helper


class BaseEmailException(BaseException):
    pass


def my():
    user = base_helper.check_auth(api.db)
    if not user.get('login'):
        return base_helper.base_response('Can not authenticate you.', 401)

    email = user.get('email')
    if not email:
        return base_helper.base_response('You did not specified your email.')
    return base_helper.base_response('Your email: {}'.format(email))


def send():
    user = base_helper.check_auth(api.db)
    if not user.get('login'):
        return base_helper.base_response('Can not authenticate you.', 401)

    args = flask.request.get_json()
    if not args:
        return base_helper.base_response(
            'Please, specify text and recipients.', 400)
    subject = args.get('subject', 'No subject')
    body = args.get('body', '')
    recipients = args.get('recipients', [])

    if not recipients:
        return base_helper.base_response('Please, specify recipients', 400)

    sender = user.get('email', api.app.config['MAIL_DEFAULT_SENDER'])
    r_text, code = helper.email_sender(api.mail, api.app,
                                       subject=subject,
                                       body=body,
                                       sender=sender,
                                       recipients=recipients)
    return base_helper.base_response(r_text, code)
