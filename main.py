from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
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
    updater = Updater("7576353277:AAEaeYsp0IAcOkTiUgmgDbWjSDKIuZj-knE")
    dispatcher = updater.dispatcher

   conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start_registration)],
    states={
        CHOOSING_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_role_choice)],
        CHOOSING_USTA_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_usta_type)],
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
        ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
        ASK_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_username)],
        SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_action)],
        USTA_SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, usta_search_action)],
    },
        fallbacks=[
            CommandHandler('start', restart),
            CommandHandler('orqaga', back),
            MessageHandler(filters.regex('^/start$'), restart),
            MessageHandler(filters.regex('^/orqaga$'), back),
        ]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()