from typing import Optional

from fast_viber_api.viber_requests import BaseRequest


class Handler:
    def __init__(self, func, events, kwargs):
        super(Handler, self).__init__()
        self.func = func
        self.events = events if isinstance(events, list) else [events]
        self.params = kwargs

    async def call(self, request: Optional[BaseRequest]):
        dict_request = request.dict()
        print(dict_request == {**dict_request, **self.params}, request.event in self.events)
        if dict_request == {**dict_request, **self.params} and request.event in self.events:
            await self.func(request)
