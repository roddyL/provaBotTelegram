from telegram.ext import ConversationHandler
from smactbot.db_functions import update_session, check_whitelist

def session_check(func):
    async def the_check(update, context):
        if update.callback_query:
            telegram_id=update.callback_query.from_user.id
        else:
            telegram_id=update.message.from_user.id

        if telegram_id not in check_whitelist():
            await context.bot.send_message(chat_id=update.effective_chat.id, text="La sessione è scaduta, ripassa per il /login !")
            context.user_data['in_conversation'] = False
            return ConversationHandler.END
        else:
            update_session(telegram_id)
            return await func(update, context)

    return the_check 
