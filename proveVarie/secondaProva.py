import telegram
bot = telegram.Bot(token='5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0')
# print(bot.get_me())
updates = bot.get_updates()
# print(updates[0])
# bot.sendMessage(text="bea",chat_id=updates[0].message.from_user.id)
for i in updates:
    print(i.message.text)