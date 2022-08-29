from firstsaturdaybot import (
    IFSCONFIGURATION,
    IFSEVENTTIME,
    IFSDATABASE
)
from firstsaturdaybot.commands.common_commads import (
    reply_message,
    set_start_over,
    remove_start_over
)
from firstsaturdaybot.handlers.security import restricted_firstsaturday
from firstsaturdaybot.handlers.ifsconstants import (
    CURRENT_USER,
    START_OVER,
    STOP_CONVERSATION,
    SELECTING_USER_ACTION,
    SET_NICKNAME,
    SET_LANGUAGE,
    REMOVE_USER,
    SHOW_PRIVACY_POLICY,
    SEND_PHOTO,
    TYPING_NICKNAME
)
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
async def user_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = '') -> str:
    user_id: int = update.effective_user.id

    if text == '':
        text = "Hi!"
        text += f"\nWelcome at the {IFSCONFIGURATION.EVENT_CITY} First Saturday"
        text += f"\nStart event time: {IFSEVENTTIME.start_time().strftime('%H:%M %Z')}"
        text += f"\nEnd event time: {IFSEVENTTIME.end_time().strftime('%H:%M %Z')}"
        if IFSCONFIGURATION.STATISTIC_FORM_LINK:
            text += f"\n<a href='{IFSCONFIGURATION.STATISTIC_FORM_LINK}'>Google form link</a>"
        if IFSCONFIGURATION.PORTAL_HUNT_SPREADSHEET_LINK:
            text += f"\n<a href='{IFSCONFIGURATION.PORTAL_HUNT_SPREADSHEET_LINK}'>Portal Hunt spreadsheet link</a>"
        text += "\nTo abort, simply type /stop."

    if IFSDATABASE.find_user(user_id):
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="Send photo", callback_data=str(SEND_PHOTO))
            ],
            [
                InlineKeyboardButton(text="Change Ingress nickname", callback_data=str(SET_NICKNAME)),
            ],
            [
                InlineKeyboardButton(text="Change language", callback_data=str(SET_LANGUAGE)),
            ],
            [
                InlineKeyboardButton(text="Privacy Policy", callback_data=str(SHOW_PRIVACY_POLICY)),
            ],
            [
                InlineKeyboardButton(text="Done", callback_data=str(STOP_CONVERSATION)),
            ]])
    else:
        IFSDATABASE.register_user(user_id, 'None')
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="Set Ingress nickname", callback_data=str(SET_NICKNAME)),
            ]])
        text += '\nPlease set your Ingress nickname before we start.'

    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=text, 
                                       reply_markup=keyboard,
                                       parse_mode=ParseMode.HTML)

    context.user_data[CURRENT_USER] = IFSDATABASE.load_user_information(user_id)

    remove_start_over(context)
    return SELECTING_USER_ACTION


async def set_nickname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Please provide your nickname:"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Return Back", callback_data=str(SELECTING_USER_ACTION))]])

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    set_start_over(context)
    return TYPING_NICKNAME


async def save_nickname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_id = update.effective_user.id
    text: str
    if IFSDATABASE.update_user(user_id, {'nickname': update.message.text}):
        text = "Ingress nickname have been changed."
    else:
        text = "Internal error"

    remove_start_over(context)

    return await user_start_command(update, context, text)


async def delete_user_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_id = update.effective_user.id
    text: str
    if IFSDATABASE.delete_user(user_id):
        text = "User data have been cleared"
        text += "\nPlease send /start to get a new keyboard."
    else:
        text = "Internal error"

    await reply_message(text, update, context)


async def show_privacy_policy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data[START_OVER] = True
    text = "Privacy policy"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Clear your data", callback_data=str(REMOVE_USER))],
        [InlineKeyboardButton(text="Return Back", callback_data=str(SELECTING_USER_ACTION))]
        ])

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SHOW_PRIVACY_POLICY
