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
login_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        LOGIN_CHECK: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_check)],
        CONTACT_NAME: [MessageHandler(filters.TEXT &~filters.COMMAND, send_contact_name)],
        CONTACT_SURNAME: [MessageHandler(filters.TEXT &~filters.COMMAND, send_contact_surname)],
        CONTACT_NUMBER: [MessageHandler(filters.TEXT &~filters.COMMAND, send_contact_number)],
        CONTACT_MAIL: [MessageHandler(filters.TEXT &~filters.COMMAND, send_contact_mail)],
        BUTTON: [CallbackQueryHandler(button)],
        LOCATION: [MessageHandler(
            filters.LOCATION & ~filters.TEXT & ~filters.COMMAND, send_location)]
    },
    fallbacks=[CommandHandler(["back"], fallback)]

)

# dispatcher add handler
application.add_handler(login_conv_handler)
