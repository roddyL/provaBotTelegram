import logging
from warnings import filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, Filters, TypeHandler, ConversationHandler

# first initialization
updater = Updater(token='5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# app func
EXIT=0

# func handler

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao, vi servirò fino alla fine")

async def exit(update: Update, context:CallbackContext):
  await  context.bot.send_message(chat_id=update.effective_chat.id, 
    text="To end type /cancel.\n Input the password:")
  if update.message.text == "fromfarmtofork":
    updater.stop()
  else:
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="Incorrect! Try again.")
  return EXIT

async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    return ConversationHandler.stop()

async def transaction(update, context):
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
  bank.log(FINISHED_TRANSACTION, amount, source_id, target_id)



# main
def main():
  
  # handler
  start_handler = CommandHandler('start', start, filters=~Filters.update.edited_message)
  """exit_conv_handler = ConversationHandler(
      entry_points=[CommandHandler("exit", exit)],
      states={
          EXIT: [exit]
      },
      fallbacks=[CommandHandler("cancel", cancel)]
  )

  dispatcher.add_handler(exit_conv_handler)
  """
  # dispatcher add handler
  dispatcher.add_handler(start_handler)
  dispatcher.add_handler(CommandHandler('transaction', transaction, block=False))

  # start
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
    main()