from telegram.ext import Updater, CommandHandler
import handlers
from config import TOKEN


def main():
    token = TOKEN
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('reg', handlers.reg))
    dispatcher.add_handler(CommandHandler('del', handlers.delete))
    dispatcher.add_handler(CommandHandler('run', handlers.run))
    dispatcher.add_handler(CommandHandler('stat', handlers.stat))
    try:
        updater.start_polling()
        updater.idle()
        print('Started polling')
    except(Exception):
        print(Exception)


if __name__ == '__main__':
    main()
