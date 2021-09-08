from typing import Optional

from fast_viber_api.user import User
from fast_viber_api.viber_requests import BaseRequest, viber_request


class Handler:
    def __init__(self, bot, func, events, kwargs, state=''):
        super(Handler, self).__init__()
        self.bot = bot
        self.func = func
        self.events = events if isinstance(events, list) else [events]
        self.params = kwargs
        self.state = state

    async def call(self, request: Optional[BaseRequest], state):
        dict_request = request.dict()
        if dict_request == {**dict_request, **self.params} and request.event in self.events \
                and (state == self.state or not self.state):

            if request.event in ['subscribed', 'conversation_started']:
                user_id = dict_request['user']['id']
            elif request.event in ['unsubscribed', 'delivered', 'seen', 'failed']:
                user_id = dict_request['user_id']
            elif request.event == 'message':
                user_id = dict_request['sender']['id']
            else:
                user_id = ''

            user = User(user_id, self.bot)
            await self.func(request, user=user)
