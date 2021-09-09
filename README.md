# FastViberApi
### Installation

```sh
python3 -m venv env
source env/bin/activate
git clone https://github.com/Worrik/FastViberApi.git
pip install ./FastViberApi
rm -rf FastViberApi
```
### Example echo bot
```py
from fastapi import FastAPI

from fast_viber_api import ViberBot, Events, ConversationStartedRequest, Message, ReceiveMessageRequest
from fast_viber_api.user import User

app = FastAPI()

bot = ViberBot(
    auth_token='your bot token',
    name='TestBot'
)

app.add_api_route("/", bot.api, methods=['POST'])


@bot.handle(event=Events.CONVERSATION_STARTED)
async def hello(request: ConversationStartedRequest, user: User):
    await user.answer(Message(text='Hello'))
    await user(state='ping')


@bot.handle(message=Message(text='ping'), state='ping')
async def ping_pong(request: ReceiveMessageRequest, user: User):
    await user.answer(Message(text='pong'))
    await user(state='end')


@bot.handle(state='end')
async def echo(request: ReceiveMessageRequest, user: User):
    await user.answer(request.message)

```
```sh
uvicorn main:app --port 8080 --reload
```
#### You can use ngrok to run locally
```sh
ngrok http 8080
```
#### Set webhook
```py
from fast_viber_api import ViberBot, Webhook, Endpoints

import asyncio


async def set_webhook():
	bot = ViberBot(
	    auth_token='your bot token',
	    name='TestBot'
	)
	await bot.send(
		Endpoints.SET_WEBHOOK,
		Webhook(url='https://*.ngrok.io/').dict()
	)
	await bot.close()

asyncio.run(set_webhook())

```
