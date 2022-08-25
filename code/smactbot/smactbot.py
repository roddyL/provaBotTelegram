# smactbot.py

from smactbot.vars import *

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    Application,
    CallbackQueryHandler
)
from smactbot.handlers import *

application = Application.builder().token(
    "5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0").arbitrary_callback_data(True).build()


# handler
start_handler = CommandHandler('start', start)
login_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("login", login)],
    states={
        LOGIN_CHECK: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_check)],
        CONTACTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_contacts)],
        MENU: [CommandHandler("menu", menu)],
        BUTTON: [CallbackQueryHandler(button)],
        LOCATION: [MessageHandler(filters.LOCATION & ~filters.TEXT & ~filters.COMMAND, send_location)],
        SEATS: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_seats)]
    },
    fallbacks=[CommandHandler(["cancel", "logout", "back"], fallback)]
)

# dispatcher add handler
application.add_handler(start_handler)
application.add_handler(login_conv_handler)