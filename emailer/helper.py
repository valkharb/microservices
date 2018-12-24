import smtplib

import flask_mail


def email_sender(
        mail,
        app,
        subject: str,
        body: str,
        recipients: list,
        sender: str):

    msg = flask_mail.Message(
        subject,
        sender=sender,
        recipients=recipients,
    )
    msg.body = body

    mail = flask_mail.Mail(app) if mail is None else mail

    try:
        mail.send(msg)
    except smtplib.SMTPAuthenticationError:
        return (
            'Please log in with your web browser and then try again.', 401
        )
    except BaseException as error:
        return (
            'Unexpected error occured while sending email. '
            'Traceback: {}'.format(error), 500
        )
    return 'Email was sent.', 200
