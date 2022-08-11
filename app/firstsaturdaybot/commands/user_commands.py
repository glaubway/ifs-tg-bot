from firstsaturdaybot.commands import *
from firstsaturdaybot.tools.security import restricted_firstsaturday
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

@restricted_firstsaturday
async def user_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"Hi {update.message.from_user.username}!\n"
    text += "Today the First Saturday"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    
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
