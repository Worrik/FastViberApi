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

from fast_viber_api import ViberBot, viber_api, Events, ConversationStartedRequest, Message, ReceiveMessageRequest


app = FastAPI()

bot = ViberBot(
    auth_token='your bot token',
    name='TestBot'
)

app.add_api_route("/viber/", viber_api(bot), methods=['POST'])


@bot.handle(events=Events.CONVERSATION_STARTED)
async def hello(request: ConversationStartedRequest):
    await bot.send_message(Message(text='Hello'), receiver=request.user.id)


@bot.handle()
async def echo(request: ReceiveMessageRequest):
    await bot.send_message(
        request.message,
        receiver=request.sender.id
    )

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
