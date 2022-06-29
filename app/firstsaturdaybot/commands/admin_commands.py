from firstsaturdaybot import RUNTIME_CONFIG
from firstsaturdaybot.commands import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

async def admin_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"Hi {update.message.from_user.username}!\n"
    if not RUNTIME_CONFIG.is_user_admin(update.message.from_user.username):
        text += "You are not allowed to see it."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return END

    buttons = [
        [
            InlineKeyboardButton(text="Set start event time", callback_data=str(START_EVENT_TIME)),
        ],
        [
            InlineKeyboardButton(text="Set end event time", callback_data=str(END_EVENT_TIME)),
        ],
        [
            InlineKeyboardButton(text="Add bot admin", callback_data=str(ADD_ADMIN)),
        ],
        [
            InlineKeyboardButton(text="Remove bot admin", callback_data=str(REMOVE_ADMIN)),
        ],
        [
            InlineKeyboardButton(text="Set link to the form", callback_data=str(SET_FORM_LINK)),
        ],
        [
            InlineKeyboardButton(text="Done", callback_data=str(END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    text += "Here you can set up some bot settings."
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        await update.message.reply_text(
            "Hi, I'm Family Bot and I'm here to help you gather information about your family."
        )
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECT_ADMIN_FEATURES

async def set_start_event_time():
    pass

async def set_end_event_time():
    pass

async def add_bot_admin():
    pass

async def remove_bot_admin():
    pass

async def set_form_link():
    pass
