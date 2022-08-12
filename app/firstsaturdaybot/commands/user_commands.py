from firstsaturdaybot import RUNTIME_CONFIG
from firstsaturdaybot.commands import *
from firstsaturdaybot.tools.security import restricted_firstsaturday
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

@restricted_firstsaturday
async def user_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, text=None):
    buttons = [
        [
            InlineKeyboardButton(text="Send photo", callback_data=str(ADD_ADMIN))
        ],
        [
            InlineKeyboardButton(text="Change Ingress nickname", callback_data=str(START_EVENT_TIME)),
        ],
        [
            InlineKeyboardButton(text="Change language", callback_data=str(SHOW_CURRENT_CONFIGURATION)),
        ],
        [
            InlineKeyboardButton(text="Privacy Policy", callback_data=str(SHOW_CURRENT_CONFIGURATION)),
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
        text += f"Welcome at our {RUNTIME_CONFIG.EVENT_CITY} First Saturday\n"
        text += f"Event start time - {RUNTIME_CONFIG.EVENT_START_TIME}\n"
        text += f"Event end time - {RUNTIME_CONFIG.EVENT_END_TIME}\n"
        text += f"Google form for statistic - {RUNTIME_CONFIG.EVENT_END_TIME}\n"
        text += f"[Google form link]({RUNTIME_CONFIG.STATISTIC_FORM_LINK})\n"
        text += f"[Portal Hunt spreadsheet link]({RUNTIME_CONFIG.PORTAL_HUNT_SPREADSHEET_LINK})\n"
        text += "To abort, simply type /stop."

    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard, parse_mode='MarkdownV2')
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard, parse_mode='MarkdownV2')

    context.user_data[START_OVER] = False
    return SELECTING_USER_ACTION