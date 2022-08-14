from firstsaturdaybot import RUNTIME_CONFIG, RUNTIME_TIME
from firstsaturdaybot.commands import *
from firstsaturdaybot.handlers.security import restricted_firstsaturday
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
    )
from telegram.ext import (
    ContextTypes
    )
from telegram.constants import (
    ParseMode
    )

@restricted_firstsaturday
async def user_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, text=None):
    buttons = [
        [
            InlineKeyboardButton(text="Send photo", callback_data=str(SEND_PHOTO))
        ],
        [
            InlineKeyboardButton(text="Set Ingress nickname", callback_data=str(SET_NICKNAME)),
        ],
        [
            InlineKeyboardButton(text="Change language", callback_data=str(SET_LANGUAGE)),
        ],
        [
            InlineKeyboardButton(text="Privacy Policy", callback_data=str(SHOW_PRIVACY_POLICY)),
        ],
        [
            InlineKeyboardButton(text="Done", callback_data=str(STOP_CONVERSATION)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    try:
        user_name = update.message.from_user.username
    except AttributeError:
        user_name = update.callback_query.from_user.username
    if text is None:
        text = f"Hi {user_name}!\n"
        text += f"Welcome at the {RUNTIME_CONFIG.EVENT_CITY} First Saturday\n"
        text += f"Start event time: {RUNTIME_TIME.start_time().strftime('%H:%M %Z')}\n"
        text += f"End event time: {RUNTIME_TIME.end_time().strftime('%H:%M %Z')}\n"
        text += f"<a href='{RUNTIME_CONFIG.STATISTIC_FORM_LINK}'>Google form link</a>\n"
        text += f"<a href='{RUNTIME_CONFIG.PORTAL_HUNT_SPREADSHEET_LINK}'>Portal Hunt spreadsheet link</a>\n"
        text += "To abort, simply type /stop."

    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    context.user_data[START_OVER] = False
    return SELECTING_USER_ACTION