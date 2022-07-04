from unittest import runner
from firstsaturdaybot import RUNTIME_CONFIG
from firstsaturdaybot.commands import *
from firstsaturdaybot.tools.users import restricted
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

@restricted
async def admin_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton(text="Set start event time", callback_data=str(START_EVENT_TIME)),
            InlineKeyboardButton(text="Set end event time", callback_data=str(END_EVENT_TIME)),
        ],
        [
            InlineKeyboardButton(text="Add bot admin", callback_data=str(ADD_ADMIN)),
            InlineKeyboardButton(text="Remove bot admin", callback_data=str(REMOVE_ADMIN)),
        ],
        [
            InlineKeyboardButton(text="Set link to the form", callback_data=str(SET_FORM_LINK)),
        ],
        [
            InlineKeyboardButton(text="Show configuration", callback_data=str(SHOW_CURRENT_CONFIGURATION)),
            InlineKeyboardButton(text="Done", callback_data=str(STOP_CONVERSATION)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)


    try:
        user_name = update.message.from_user.username
    except AttributeError:
        user_name = update.callback_query.from_user.username

    text = f"Hi {user_name}!\n"
    text += "I'm FirstSaturday Bot and I'm here to help you gather information about event participants.\n"
    text += "In this menu, you can easily customize me.\n"
    text += "To abort, simply type /stop."
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_ADMIN_ACTION

@restricted
async def set_event_configuration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[START_OVER] = True
    context.user_data[CURRENT_FEATURE] = update.callback_query.data

    if update.callback_query.data == str(START_EVENT_TIME):
        text = f"Please provide start event time in the next format HH:MM."
    elif update.callback_query.data == str(END_EVENT_TIME):
        text = f"Please provide end event time in the next format HH:MM."
    elif update.callback_query.data == str(ADD_ADMIN):
        text = f"Please provide admin nickname (start with @) which should be added\n"
        text += f"Current admins: {RUNTIME_CONFIG.list_of_admins()}"
    elif update.callback_query.data == str(REMOVE_ADMIN):
        text = f"Please provide admin nickname (start with @) which should be removed\n"
        text += f"Current admins: {RUNTIME_CONFIG.list_of_admins()}"
    elif update.callback_query.data == str(SET_FORM_LINK):
        text = f"Please provide new link to the Google form.\n"
        text += f"Current link: {RUNTIME_CONFIG.FORM_LINK}"

    buttons = [[InlineKeyboardButton(text="Return Back", callback_data=str(TO_START))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return TYPING_CONFIGURATION

@restricted
async def incorrect_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Incorrect input, returning back."
    await update.message.reply_text(text=text)

    context.user_data.clear()

    return await admin_start_command(update, context)

@restricted
async def save_configuration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_message = update.message.text
    if user_data[CURRENT_FEATURE] == str(START_EVENT_TIME):
        RUNTIME_CONFIG.set_start_time(user_message)
    elif user_data[CURRENT_FEATURE] == str(END_EVENT_TIME):
        RUNTIME_CONFIG.set_end_time(user_message)
    elif user_data[CURRENT_FEATURE] == str(ADD_ADMIN):
        if not RUNTIME_CONFIG.is_user_admin(user_message):
            RUNTIME_CONFIG.add_admin(user_message[1:])
            text = f"User {user_message} have been added."
        else:
            text = f"User {user_message} is already admin."
        await update.message.reply_text(text=text)
    elif user_data[CURRENT_FEATURE] == str(REMOVE_ADMIN):
        if RUNTIME_CONFIG.is_user_admin(user_message):
            RUNTIME_CONFIG.remove_admin(user_message[1:])
            text = f"User {user_message} have been removed."
        else:
            text = f"User {user_message} isn't admin."
        await update.message.reply_text(text=text)
    elif user_data[CURRENT_FEATURE] == str(SET_FORM_LINK):
        RUNTIME_CONFIG.set_form_link(user_message)

    context.user_data.clear()
    del user_data
    del user_message
    return await admin_start_command(update, context)

@restricted
async def show_current_configuration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data[START_OVER] = True
    
    text = f"The current configuration of bot is next:\n"
    text += f"Start event time: {RUNTIME_CONFIG.EVENT_START_TIME}\n"
    text += f"End event time: {RUNTIME_CONFIG.EVENT_END_TIME}\n"
    text += f"Current timezone: {RUNTIME_CONFIG.EVENT_TIMEZONE}\n"
    text += f"Current city: {RUNTIME_CONFIG.EVENT_CITY}\n"
    text += f"Admins username: {RUNTIME_CONFIG.list_of_admins()}\n"
    text += f"Google form link: {RUNTIME_CONFIG.FORM_LINK}\n"

    buttons = [[InlineKeyboardButton(text="Return Back", callback_data=str(TO_START))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SHOW_CURRENT_CONFIGURATION