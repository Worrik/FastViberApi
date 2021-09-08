class User:
    methods = ['user_id', 'redis_machine', 'answer', 'bot']

    def __init__(self, user_id, bot):
        self.user_id = user_id
        self.redis_machine = bot.redis_machine
        self.bot = bot

    def __setattr__(self, key, value):
        if key not in self.methods:
            return self.redis_machine.update_data(self.user_id, key=value)
        self.__dict__[key] = value

    def __call__(self, *args, **kwargs):
        return self.redis_machine.update_data(self.user_id, **kwargs)

    def __getattr__(self, item):
        if item not in self.methods:
            return self.redis_machine.get_value(self.user_id, item)
        return self.__dict__[item]

    def __getitem__(self, item):
        return self.redis_machine.get_value(self.user_id, item)

    async def answer(self, message):
        return await self.bot.send_message(message, self.user_id)
