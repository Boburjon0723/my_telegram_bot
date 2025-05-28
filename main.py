from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
from handlers.registration import (
    start_registration,
    handle_role_choice,
    handle_usta_type,
    ask_name,
    ask_phone,
    ask_username,
    search_action,
    usta_search_action,
    back,
    restart,
    CHOOSING_ROLE,
    CHOOSING_USTA_TYPE,
    ASK_NAME,
    ASK_PHONE,
    ASK_USERNAME,
    SEARCH,
    USTA_SEARCH
)
import database

def main():
    database.init_db()
    updater = Updater("7576353277:AAEOUM17xRrQdypjsaf3yqHOrrQYRVA_MiM", use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_registration)],
        states={
            CHOOSING_ROLE: [MessageHandler(Filters.text & ~Filters.command, handle_role_choice)],
            CHOOSING_USTA_TYPE: [MessageHandler(Filters.text & ~Filters.command, handle_usta_type)],
            ASK_NAME: [MessageHandler(Filters.text & ~Filters.command, ask_name)],
            ASK_PHONE: [MessageHandler(Filters.text & ~Filters.command, ask_phone)],
            ASK_USERNAME: [MessageHandler(Filters.text & ~Filters.command, ask_username)],
            SEARCH: [MessageHandler(Filters.text & ~Filters.command, search_action)],
            USTA_SEARCH: [MessageHandler(Filters.text & ~Filters.command, usta_search_action)],
        },
        fallbacks=[
            CommandHandler('start', restart),
            CommandHandler('orqaga', back),
            MessageHandler(Filters.regex('^/start$'), restart),
            MessageHandler(Filters.regex('^/orqaga$'), back),
        ]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()