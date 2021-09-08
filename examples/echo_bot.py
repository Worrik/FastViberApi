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


@bot.handle(message=Message(text='ping'), state='ping')
async def ping_pong(request: ReceiveMessageRequest, user: User):
    await user.answer(Message(text='pong'))
    await user(state='end')


@bot.handle(state='end')
async def echo(request: ReceiveMessageRequest, user: User):
    await user.answer(request.message)
