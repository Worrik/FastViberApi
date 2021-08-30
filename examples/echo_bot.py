from fastapi import FastAPI

from fast_viber_api import ViberBot, viber_api, Events, ConversationStartedRequest, Message, ReceiveMessageRequest


app = FastAPI()

bot = ViberBot(
    auth_token='your bot token',
    name='TestBot'
)

app.add_api_route("/", viber_api(bot), methods=['POST'])


@bot.handle(events=Events.CONVERSATION_STARTED)
async def hello(request: ConversationStartedRequest):
    await bot.send_message(Message(text='Hello'), receiver=request.user.id)


@bot.handle()
async def echo(request: ReceiveMessageRequest):
    await bot.send_message(
        request.message,
        receiver=request.sender.id
    )
