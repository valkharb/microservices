import os

import flask
import requests
import telebot

import api
import base_helper

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')


def my():
    user = base_helper.check_auth(api.db)
    if not user.get('login'):
        return base_helper.base_response('Can not authenticate you.', 401)

    nickname = user.get('nickname')
    if not nickname:
        return base_helper.base_response('You did not specified your nickname.')

    nickname = '@' + nickname if nickname[0] != '@' else nickname
    return base_helper.base_response('Your nickname: {}'.format(nickname))


def send():
    user = base_helper.check_auth(api.db)
    if not user.get('login'):
        return base_helper.base_response('Can not authenticate you.', 401)

    args = flask.request.get_json()
    if not args:
        return base_helper.base_response(
            'Please, specify text for sending and chat id.', 400)

    text = args.get('text', 'Test text')
    chat_id = args.get('chat_id', '')
    if not chat_id:
        return base_helper.base_response('Please, specify chat id', 400)

    bot = telebot.TeleBot(TELEGRAM_TOKEN)

    try:
        bot.send_message(
            chat_id=chat_id,
            text=text,
        )
    except telebot.apihelper.ApiException as err:
        return base_helper.base_response(
            'Telebot exception has occured. Traceback: {}'.format(err), 500)
    except requests.exceptions.ConnectionError:
        return base_helper.base_response('Max retries exceeded.', 400)

    return base_helper.base_response('Text was sent.')
