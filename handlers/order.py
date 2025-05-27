from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext
)

SERVICE, PHONE, LOCATION = range(3)

def start_order(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Buyurtma uchun xizmat turini tanlang:",
        reply_markup=ReplyKeyboardMarkup(
            [["Fundament", "G'isht quyish"], ["Malyarka", "Santexnika"]],
            one_time_keyboard=True
        )
    )
    return SERVICE

def receive_service(update: Update, context: CallbackContext) -> int:
    context.user_data['service'] = update.message.text
    update.message.reply_text(
        "Telefon raqamingizni yuboring:",
        reply_markup=ReplyKeyboardRemove()
    )
    return PHONE

def receive_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['phone'] = update.message.text
    update.message.reply_text("Manzilingizni yuboring:")
    return LOCATION

def receive_location(update: Update, context: CallbackContext) -> int:
    context.user_data['location'] = update.message.text
    user_data = context.user_data
    order_info = (
        f"📝 Yangi buyurtma:\n\n"
        f"🔧 Xizmat: {user_data['service']}\n"
        f"📞 Telefon: {user_data['phone']}\n"
        f"📍 Manzil: {user_data['location']}"
    )
    update.message.reply_text(
        f"Buyurtmangiz qabul qilindi!\n\n{order_info}"
    )
    return ConversationHandler.END

def cancel_order(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Buyurtma bekor qilindi.")
    return ConversationHandler.END

order_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('order', start_order)],
    states={
        SERVICE: [MessageHandler(Filters.text & ~Filters.command, receive_service)],
        PHONE: [MessageHandler(Filters.text & ~Filters.command, receive_phone)],
        LOCATION: [MessageHandler(Filters.text & ~Filters.command, receive_location)]
    },
    fallbacks=[CommandHandler('cancel', cancel_order)]
)