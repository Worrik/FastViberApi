import asyncio
import hashlib
import hmac
import logging
import ssl
from typing import Optional, Union

import aiohttp
import certifi
from starlette.requests import Request

from fast_viber_api.handler import Handler
from fast_viber_api.redis_machine import RedisMachine
from fast_viber_api.user import User
from fast_viber_api.viber_requests import BotConfiguration, BaseMessage, BaseRequest, viber_request

VIBER_BOT_API_URL = "https://chatapi.viber.com/pa"

logging.root.setLevel(logging.NOTSET)


class Endpoints:
    SET_WEBHOOK = 'set_webhook'
    GET_ACCOUNT_INFO = 'get_account_info'
    SEND_MESSAGE = 'send_message'
    GET_ONLINE = 'get_online'
    GET_USER_DETAILS = 'get_user_details'
    POST = 'post'


class Events:
    WEBHOOK = 'webhook'
    SUBSCRIBED = 'subscribed'
    UNSUBSCRIBED = 'unsubscribed'
    CONVERSATION_STARTED = 'conversation_started'
    DELIVERED = 'delivered'
    SEEN = 'seen'
    FAILED = 'failed'
    MESSAGE = 'message'


class ViberBot:
    api_url = VIBER_BOT_API_URL

    def __init__(self, auth_token, name, connections_limit=None, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.redis_machine = RedisMachine()
        self.bot_configuration = BotConfiguration(
            auth_token=auth_token,
            name=name
        )

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(limit=connections_limit, ssl_context=ssl_context,
                                         loop=self.loop)

        self.session = aiohttp.ClientSession(connector=connector, loop=self.loop)
        self.handlers = []

    async def close(self):
        await self.session.close()

    def clean(self, message):
        return {k: self.clean(v) if isinstance(v, dict) else v for k, v in message.items() if v is not None}

    async def send_message(self, message: Union[BaseMessage, dict], receiver: str = ""):
        if isinstance(message, dict):
            payload = self.clean(message)
        else:
            payload = self.clean(message.dict())

        if receiver:
            payload['receiver'] = receiver

        return await self.send(Endpoints.SEND_MESSAGE, payload)

    async def send(self, uri, payload):
        url = f"{self.api_url}/{uri}"

        payload = {**self.bot_configuration.dict(),
                   **payload}

        async with self.session.post(url, json=payload) as response:
            return await response.json()

    def verify_signature(self, request_data, signature):
        return signature == self._calculate_message_signature(request_data)

    def _calculate_message_signature(self, message):
        return hmac.new(
            bytes(self.bot_configuration.auth_token.encode('ascii')),
            msg=message, digestmod=hashlib.sha256).hexdigest()

    def handle(self, event='message', state='', **kwargs):
        def decorator(func):
            self.handlers.append(Handler(self, func, event, kwargs, state=state))
            return func

        return decorator

    def get_user(self, request):
        dict_request = request.dict()
        if request.event in ['subscribed', 'conversation_started']:
            user_id = dict_request['user']['id']
        elif request.event in ['unsubscribed', 'delivered', 'seen', 'failed']:
            user_id = dict_request['user_id']
        elif request.event == 'message':
            user_id = dict_request['sender']['id']
        else:
            user_id = ''

        return User(user_id, self)

    async def call_handlers(self, request: Optional[BaseRequest], state):
        for handler in self.handlers:
            await handler.call(request, state)

    async def api(self, viber: viber_request, request: Request):
        text = await request.body()
        sig = request.query_params.get('sig')

        logging.info("ViberRequest: %s", viber)

        if not self.verify_signature(text, sig):
            logging.warning("Invalid signature")
            return

        user = self.get_user(viber)
        await self.call_handlers(viber, await user.state)
