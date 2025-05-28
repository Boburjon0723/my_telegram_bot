from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

CHOOSING_ROLE, CHOOSING_USTA_TYPE, ASK_NAME, ASK_PHONE, ASK_USERNAME, SEARCH, USTA_SEARCH = range(7)

SOHA_LIST = [
    ["Santexnik", "Elektrik"],
    ["Malyarkachi", "Betonchi"],
    ["G'isht quyish", "Quruvchi"]
]

def get_keyboard(extra=None):
    keyboard = []
    if extra:
        keyboard += extra
    keyboard.append(["/start", "/orqaga"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def start_registration(update, context):
    update.message.reply_text(
        "Rolingizni tanlang:",
        reply_markup=get_keyboard([["Ustaman", "Buyurtmachiman"]])
    )
    context.user_data['last_state'] = CHOOSING_ROLE
    return CHOOSING_ROLE

def handle_role_choice(update, context):
    role = update.message.text
    context.user_data['role'] = role
    context.user_data['last_state'] = CHOOSING_ROLE
    if role == "Ustaman":
        update.message.reply_text(
            "Qaysi soha ustasisiz?",
            reply_markup=get_keyboard(SOHA_LIST)
        )
        context.user_data['last_state'] = CHOOSING_USTA_TYPE
        return CHOOSING_USTA_TYPE
    elif role == "Buyurtmachiman":
        update.message.reply_text(
            "Ismingizni kiriting:", reply_markup=get_keyboard()
        )
        context.user_data['last_state'] = ASK_NAME
        return ASK_NAME
    else:
        update.message.reply_text("Iltimos, tugmalardan birini tanlang.", reply_markup=get_keyboard([["Ustaman", "Buyurtmachiman"]]))
        return CHOOSING_ROLE

def handle_usta_type(update, context):
    usta_type = update.message.text
    context.user_data['usta_type'] = usta_type
    context.user_data['last_state'] = CHOOSING_USTA_TYPE
    update.message.reply_text(
        "Ismingizni kiriting:", reply_markup=get_keyboard()
    )
    context.user_data['last_state'] = ASK_NAME
    return ASK_NAME

def ask_name(update, context):
    context.user_data['name'] = update.message.text
    context.user_data['last_state'] = ASK_NAME
    update.message.reply_text("Telefon raqamingizni kiriting:", reply_markup=get_keyboard())
    context.user_data['last_state'] = ASK_PHONE
    return ASK_PHONE

def ask_phone(update, context):
    context.user_data['phone'] = update.message.text
    context.user_data['last_state'] = ASK_PHONE
    update.message.reply_text("Telegram global nomingizni (username) kiriting (masalan: @username):", reply_markup=get_keyboard())
    context.user_data['last_state'] = ASK_USERNAME
    return ASK_USERNAME

import database
# ...existing code...

def ask_username(update, context):
    context.user_data['username'] = update.message.text
    user_data = context.user_data

    # Foydalanuvchini bazaga yozish
    is_usta = user_data.get('role') == "Ustaman"
    user_id = database.save_user(
        telegram_id=update.effective_user.id,
        full_name=user_data.get('name'),
        phone=user_data.get('phone'),
        username=user_data.get('username'),
        is_usta=is_usta
    )
    # Agar usta bo‘lsa, sohasini ham bog‘lash
    if is_usta:
        database.save_usta_skill(user_id, user_data.get('usta_type'))

    info = (
        f"✅ Ro'yxatdan o'tdingiz!\n\n"
        f"Ism: {user_data.get('name')}\n"
        f"Telefon: {user_data.get('phone')}\n"
        f"Telegram: {user_data.get('username')}\n"
    )
    if is_usta:
        info += f"Usta yo'nalishi: {user_data.get('usta_type')}\n"
        update.message.reply_text(
            info + "\nEndi siz ish qidirishingiz mumkin:",
            reply_markup=get_keyboard([["Ish qidirish"]])
        )
        context.user_data['last_state'] = SEARCH
        return SEARCH
    else:
        update.message.reply_text(
            info + "\nEndi siz usta qidirishingiz mumkin:",
            reply_markup=get_keyboard([["Usta qidirish"]])
        )
        context.user_data['last_state'] = SEARCH
        return SEARCH

def search_action(update, context):
    role = context.user_data.get('role')
    context.user_data['last_state'] = SEARCH
    if role == "Ustaman":
        update.message.reply_text("Siz uchun ishlar ro‘yxati hozircha mavjud emas (demo).", reply_markup=get_keyboard())
        return ConversationHandler.END
    else:
        update.message.reply_text(
            "Qaysi soha bo‘yicha usta qidiryapsiz?",
            reply_markup=get_keyboard(SOHA_LIST)
        )
        context.user_data['last_state'] = USTA_SEARCH
        return USTA_SEARCH

def usta_search_action(update, context):
    soha = update.message.text
    context.user_data['last_state'] = USTA_SEARCH
    ustalar = database.find_ustalar_by_skill(soha)
    if ustalar:
        text = f"{soha} sohasidagi ustalar ro‘yxati:\n\n"
        for i, (name, phone, username) in enumerate(ustalar, 1):
            text += f"{i}. {name} | {phone} | {username}\n"
    else:
        text = f"{soha} sohasida hozircha usta topilmadi."
    update.message.reply_text(text, reply_markup=get_keyboard())
    return ConversationHandler.END

def restart(update, context):
    context.user_data.clear()
    return start_registration(update, context)

def back(update, context):
    state = context.user_data.get('last_state')
    if state == CHOOSING_USTA_TYPE:
        return start_registration(update, context)
    elif state == ASK_NAME:
        role = context.user_data.get('role')
        if role == "Ustaman":
            update.message.reply_text(
                "Qaysi soha ustasisiz?",
                reply_markup=get_keyboard(SOHA_LIST)
            )
            context.user_data['last_state'] = CHOOSING_USTA_TYPE
            return CHOOSING_USTA_TYPE
        else:
            return start_registration(update, context)
    elif state == ASK_PHONE:
        update.message.reply_text("Ismingizni kiriting:", reply_markup=get_keyboard())
        context.user_data['last_state'] = ASK_NAME
        return ASK_NAME
    elif state == ASK_USERNAME:
        update.message.reply_text("Telefon raqamingizni kiriting:", reply_markup=get_keyboard())
        context.user_data['last_state'] = ASK_PHONE
        return ASK_PHONE
    elif state == SEARCH:
        role = context.user_data.get('role')
        if role == "Ustaman":
            update.message.reply_text("Ismingizni kiriting:", reply_markup=get_keyboard())
            context.user_data['last_state'] = ASK_NAME
            return ASK_NAME
        else:
            update.message.reply_text("Telefon raqamingizni kiriting:", reply_markup=get_keyboard())
            context.user_data['last_state'] = ASK_PHONE
            return ASK_PHONE
    elif state == USTA_SEARCH:
        update.message.reply_text(
            "Qaysi soha bo‘yicha usta qidiryapsiz?",
            reply_markup=get_keyboard(SOHA_LIST)
        )
        context.user_data['last_state'] = USTA_SEARCH
        return USTA_SEARCH
    else:
        return start_registration(update, context)