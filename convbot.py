import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

TOKEN = "1485482332:AAHmcJJf1uFjfhEDxDQAK3m6eb4lOTb2LhE"


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Возраст', 'Любимый цвет'],
    ['Число братьев/сестер', 'Что-то еще...'],
    ['Закончить'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)



def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет, меня зовут Bot, я хочу поговорить с тобой. О чем о себе бы ты хотел бы рассказать?",
        reply_markup=markup,
    )
    return CHOOSING


def regular_choice(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        # f'Про {text.lower()}? Да, я хотел бы об этом узнать!'
        f'Да, я хотел бы об этом узнать!'
    )
    return TYPING_REPLY


def custom_choice(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Хорошо, но пришли мне сначала категорию ' 'например "Что я умею лучше всего"'
    )
    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(
        f"Аккуратно! Просто чтобы вы знали, вот что вы мне уже сказали:"
        f"{facts_to_str(user_data)} Вы можете рассказать мне больше или изменить свое мнение"
        " о чем-нибудь.",
        reply_markup=markup,
    )

    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"Я узнал о тебе следующее:" f"{facts_to_str(user_data)}" "До встречи!"
    )

    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Возраст|Любимый цвет|Число братьев/сестер)$'), regular_choice
                ),
                MessageHandler(Filters.regex('^Что-то еще...$'), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Закончить')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Закончить$')),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Закончить$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()