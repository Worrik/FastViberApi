import asyncio
import hashlib
import hmac
import ssl
from typing import Optional, Union

import aiohttp
import certifi

from fast_viber_api.handler import Handler
from fast_viber_api.viber_requests import BotConfiguration, BaseMessage, BaseRequest

VIBER_BOT_API_URL = "https://chatapi.viber.com/pa"
VIBER_BOT_USER_AGENT = "ViberBot-Python/0.0.1"


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
    user_agent = VIBER_BOT_USER_AGENT

    def __init__(self, auth_token, name, connections_limit=None, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
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
        headers = {
            'User-Agent': self.user_agent
        }
        url = f"{self.api_url}/{uri}"

        payload = {**self.bot_configuration.dict(),
                   **payload}

        async with self.session.post(url, json=payload, headers=headers) as response:
            return await response.json()

    def verify_signature(self, request_data, signature):
        return signature == self._calculate_message_signature(request_data)

    def _calculate_message_signature(self, message):
        return hmac.new(
            bytes(self.bot_configuration.auth_token.encode('ascii')),
            msg=message, digestmod=hashlib.sha256).hexdigest()

    def handle(self, events='message', **kwargs):
        def decorator(coro):
            self.handlers.append(Handler(coro, events, kwargs))

        return decorator

    async def call_handlers(self, request: Optional[BaseRequest]):
        for handler in self.handlers:
            await handler.call(request)
