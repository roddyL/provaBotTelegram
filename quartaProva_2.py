import logging
from warnings import filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, filters, TypeHandler, ConversationHandler, Application

# first initialization
application = Application.builder().token("5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0").build()
"""updater = Updater(token="5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0", use_context=True)"""
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# app func
EXIT=range(1)

# func handler

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Ciao, vi servirò fino alla fine")

async def exit(update: Update, context:CallbackContext):
  await  context.bot.send_message(chat_id=update.effective_chat.id, 
    text="To end type /cancel.\n Input the password:")
  if update.message.text == "fromfarmtofork":
    context.bot.send_message(chat_id=update.effective_chat.id, 
    text="CiaoCiao!")
    application.close()
    return ConversationHandler.END
  else:
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="Incorrect! Try again.")
    return EXIT

async def kill(update: Update, context:CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, 
    text="CiaoCiao!")
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Cancelled succesfully."
    )

    return ConversationHandler.END

"""async def transaction(update, context):
  bot = context.bot
  chat_id = update.effective_user.id
  source_id, target_id, amount = parse_update(update)

  await bot.send_message(chat_id, 'Preparing...')
  bank.log(BEGINNING_TRANSACTION, amount, source_id, target_id)

  source = bank.read_account(source_id)
  target = bank.read_account(target_id)

  source.balance -= amount
  target.balance += amount

  await bot.send_message(chat_id, 'Transferring money...')
  bank.log(CALCULATED_TRANSACTION, amount, source_id, target_id)

  bank.write_account(source)
  await bot.send_message(chat_id, 'Source account updated...')
  await bot.send_message(chat_id, 'Target account updated...')
  bank.write_account(target)
  
  await bot.send_message(chat_id, 'Done!')
  bank.log(FINISHED_TRANSACTION, amount, source_id, target_id)"""



# main
def main():
  
  # handler
  start_handler = CommandHandler('start', start)
  exit_conv_handler = ConversationHandler(
      entry_points=[CommandHandler("exit", exit)],
      states={
          EXIT: [MessageHandler(filters.Regex("^(fromfarmtofork)$"),kill), MessageHandler(not filters.Regex("^(fromfarmtofork)$"), exit)]
      },
      fallbacks=[CommandHandler("cancel", cancel)]
  )

  application.add_handler(exit_conv_handler)
  
  # dispatcher add handler
  application.add_handler(start_handler)
  """dispatcher.add_handler(CommandHandler('transaction', transaction, block=False))"""

  # start
  application.run_polling()

if __name__ == '__main__':
    main()