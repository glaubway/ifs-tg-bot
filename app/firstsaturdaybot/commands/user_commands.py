from firstsaturdaybot.commands import *
from firstsaturdaybot.tools.timemodule import is_firstsaturday
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler


async def select_user_feature(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    buttons = [
        [
            InlineKeyboardButton(text="Set start event time", callback_data=str(SET_NICKNAME)),
        ],
        [
            InlineKeyboardButton(text="Set end event time", callback_data=str(REMOVE_NICKNAME)),
        ],
        [
            InlineKeyboardButton(text="Add bot admin", callback_data=str(SEND_PHOTO)),
        ],
        [
            InlineKeyboardButton(text="Done", callback_data=str(END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    text = "Got it! Please select a feature to update."
    await update.message.reply_text(text=text, reply_markup=keyboard)
    return SELECT_ADMIN_FEATURES
