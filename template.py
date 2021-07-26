import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = # напишите сюда свой токен

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Привет!')


def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text()


def main():
    # Создает Updater и привязывает к боту
    updater = Updater(TOKEN, use_context=True)

    # Для работы функций
    dispatcher = updater.dispatcher

    # стандратные команды
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # пользовательские функции

    # стартуем бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()