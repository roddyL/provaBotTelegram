from telegram import CallbackQuery, Update
from smactbot.TgButtonInterface import TgButtonInterface
from smactbot.db_functions import change_role
from smactbot.vars import BUTTON
from smactbot.db_functions import update_session, check_whitelist, check_authorization
from smactbot.log import logger


def session_check(func):
    async def the_check(update, context):
        if update.callback_query:
            telegram_id = update.callback_query.from_user.id
        else:
            telegram_id = update.message.from_user.id

        if check_whitelist(telegram_id=telegram_id) == 0:
            # additionalText="La sessione è scaduta, ripassa per il login!"
            # interfaccia = menu_interface_main(autorizzazioni=return_auth(telegram_id=telegram_id),additionalText=additionalText)
            # # context.user_data['in_conversation'] = False
            # if update.callback_query:
            #     await update.callback_query.edit_message_text(text=interfaccia[0],
            #                         reply_markup=interfaccia[1])
            # else:
            #     await update.message.reply_text(text=interfaccia[0],
            #                         reply_markup=interfaccia[1])
            # update_session(telegram_id)
            # return BUTTON
            if update.callback_query:
                update.callback_query.data = "logout"
            else:
                additionalText = "La sessione è scaduta, ripassa per il login!"
                interfaccia = TgButtonInterface.main_menu(role_authorization=check_authorization(
                    telegram_id=telegram_id), additional_text=additionalText)
                await update.message.reply_text(text=interfaccia[0],
                                                reply_markup=interfaccia[1])
                update_session(telegram_id=telegram_id)
                change_role(telegram_id=telegram_id, role_name="guest")

                return BUTTON

        update_session(telegram_id)
        return await func(update, context)

    return the_check


def get_log(func):
    async def make_log(update: Update, context: CallbackQuery):
        if update.message:
            message = update.message
            if message.location:
                logger.info(
                    f"- Method: {func.__name__} "\
                        f"- User: {message.from_user.username} "\
                            f"- TelegramId: {message.from_user.id} "\
                                f"- ChatId: {message.chat_id} "\
                                    f"- Location: {message.location}")
            elif message.text:
                logger.info(
                    f"- Method: {func.__name__} "\
                        f"- User: {message.from_user.username} "\
                            f"- TelegramId: {message.from_user.id} "\
                                f"- ChatId: {message.chat_id} "\
                                    f"- Text: {message.text}")
        else:
            message = update.callback_query
            logger.info(
                f"- Method: {func.__name__} "\
                        f"- User: {message.from_user.username} "\
                            f"- TelegramId: {message.from_user.id} "\
                                f"- ChatId: {message.message.chat_id} "\
                                    f"- CallbackQuery: {message.data}")
        
        return await func(update, context)

    return make_log


def delete_old_messages(func):

    pass
