# smactbot.py

from smactbot.vars import (
    BUTTON,
    LOGIN_CHECK,
    MENU
)
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    Application,
    CallbackQueryHandler
)
from smactbot.handlers import (
    start,
    login,
    login_check,
    menu,
    button,
    fallback
)

application = Application.builder().token(
    "5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0").build()


# handler
start_handler = CommandHandler('start', start)
login_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("login", login)],
    states={
        LOGIN_CHECK: [MessageHandler(filters.TEXT, login_check)],
        MENU: [CommandHandler("menu", menu)],
        BUTTON: [CallbackQueryHandler(button)],
    },
    fallbacks=[CommandHandler(["cancel", "logout"], fallback)]
)

# dispatcher add handler
application.add_handler(start_handler)
application.add_handler(login_conv_handler)
