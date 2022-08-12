from firstsaturdaybot import RUNTIME_CONFIG, RUNTIME_TIME
from firstsaturdaybot.commands import *
from firstsaturdaybot.tools.security import restricted_admin
from firstsaturdaybot.tools.logger import myLogger
from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Update
)
from telegram.ext import (
    ContextTypes
)

logger = myLogger(__name__)

@restricted_admin
async def admin_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, text=None):
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
            InlineKeyboardButton(text="Statistic form link", callback_data=str(SET_STATISTIC_FORM_LINK)),
            InlineKeyboardButton(text="Portal Hunt link", callback_data=str(SET_PORTAL_HUNT_SPREADSHEET_LINK)),
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
    if text is None:
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

@restricted_admin
async def set_event_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[START_OVER] = True
    context.user_data[CURRENT_FEATURE] = update.callback_query.data

    if update.callback_query.data == str(START_EVENT_TIME):
        text = f"Please provide start event time in the next format HH:MM."
    elif update.callback_query.data == str(END_EVENT_TIME):
        text = f"Please provide end event time in the next format HH:MM."
    else:
        return await incorrect_input(update, context) 

    buttons = [[InlineKeyboardButton(text="Return Back", callback_data=str(TO_START))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return TYPING_TIME_CONFIGURATION

@restricted_admin
async def set_event_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[START_OVER] = True
    context.user_data[CURRENT_FEATURE] = update.callback_query.data
    NEXT_STAGE = None

    if update.callback_query.data == str(ADD_ADMIN):
        text = f"Please provide admin nickname which should be added\n"
        text += f"Current admins: {RUNTIME_CONFIG.show_current_admins_as_string()}"
        buttons = [[InlineKeyboardButton(text="Return Back", callback_data=str(TO_START))]]
        NEXT_STAGE = TYPING_ADD_ADMIN
    elif update.callback_query.data == str(REMOVE_ADMIN):
        text = f"Please choose admin nickname which should be removed\n"
        text += f"Current admins:"
        buttons = []
        for admin_nickname in RUNTIME_CONFIG.show_current_admins_as_list():
            if not RUNTIME_CONFIG.is_user_predefined_admin(admin_nickname):
                buttons.append(
                [InlineKeyboardButton(text=str(admin_nickname), callback_data=str(admin_nickname))]
                )
        buttons.append([InlineKeyboardButton(text="Return Back", callback_data=str(TO_START))])
        NEXT_STAGE = TYPING_REMOVE_ADMIN
    else:
        return await incorrect_input(update, context) 
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return NEXT_STAGE

@restricted_admin
async def set_event_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[START_OVER] = True
    context.user_data[CURRENT_FEATURE] = update.callback_query.data
    NEXT_STAGE = None

    if update.callback_query.data == str(SET_STATISTIC_FORM_LINK):
        text = f"Please provide new link to the Google form.\n"
        text += f"Current link: {RUNTIME_CONFIG.STATISTIC_FORM_LINK}"
        NEXT_STAGE = TYPING_STATISTIC_SPREADSHEET_LINK
    elif update.callback_query.data == str(SET_PORTAL_HUNT_SPREADSHEET_LINK):
        text = f"Please provide new link to the Portal Hunt spreadsheet.\n"
        text += f"Current link: {RUNTIME_CONFIG.PORTAL_HUNT_SPREADSHEET_LINK}"
        NEXT_STAGE = TYPING_PORTAL_HUNT_SPREADSHEET_LINK
    else:
        return await incorrect_input(update, context) 

    buttons = [[InlineKeyboardButton(text="Return Back", callback_data=str(TO_START))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return NEXT_STAGE


@restricted_admin
async def incorrect_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Incorrect input, returning back."
    await update.message.reply_text(text=text)

    context.user_data.clear()

    return await admin_start_command(update, context)

@restricted_admin
async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if not RUNTIME_CONFIG.is_user_admin(user_message):
        RUNTIME_CONFIG.add_admin(user_message)
        text = f"User {user_message} have been added t admin list."
    else:
        text = f"User {user_message} is already admin."

    context.user_data.clear()
    return await admin_start_command(update, context, text)

@restricted_admin
async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.callback_query.data
    
    if RUNTIME_CONFIG.remove_admin(user_message):
        text = f"User {user_message} has been removed from admin list."
    else:
        text = f"User {user_message} hasn't been removed."
    
    context.user_data.clear()
    context.user_data[START_OVER] = True
    await admin_start_command(update, context, text)

@restricted_admin
async def save_time_configuration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if context.user_data[CURRENT_FEATURE] == str(START_EVENT_TIME):
        if RUNTIME_TIME.set_start_time(user_message):
            text = f"The new star event time is {user_message}"
        else:
            text = f"Start time should be less then end time"
    elif context.user_data[CURRENT_FEATURE] == str(END_EVENT_TIME):
        if RUNTIME_TIME.set_end_time(user_message):
            text = f"The new end event time is {user_message}"
        else:
            text = f"End time should be more then end time"
    
    context.user_data.clear()
    return await admin_start_command(update, context, text)

@restricted_admin
async def save_link_configuration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if context.user_data[CURRENT_FEATURE] == str(SET_STATISTIC_FORM_LINK):
        RUNTIME_CONFIG.set_statistic_form_link(user_message)
    elif context.user_data[CURRENT_FEATURE] == str(SET_PORTAL_HUNT_SPREADSHEET_LINK):
        RUNTIME_CONFIG.set_portal_hunt_spreadsheet_link(user_message)
    
    text = "The link have been changed."

    context.user_data.clear()
    return await admin_start_command(update, context, text)


@restricted_admin
async def show_current_configuration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data[START_OVER] = True
    
    text = f"The current configuration of the bot is next:\n"
    text += f"Start event time: {RUNTIME_TIME.start_time().time()}\n"
    text += f"End event time: {RUNTIME_TIME.end_time().time()}\n"
    text += f"Current timezone: {RUNTIME_TIME.EVENT_TIMEZONE}\n"
    text += f"Current city: {RUNTIME_CONFIG.EVENT_CITY}\n"
    text += f"Admins username: {RUNTIME_CONFIG.show_current_admins_as_string()}\n"
    text += f"[Google form link]({RUNTIME_CONFIG.STATISTIC_FORM_LINK})\n"
    text += f"[Portal Hunt spreadsheet link]({RUNTIME_CONFIG.PORTAL_HUNT_SPREADSHEET_LINK})\n"

    buttons = [[InlineKeyboardButton(text="Return Back", callback_data=str(TO_START))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard, parse_mode='MarkdownV2')

    return SHOW_CURRENT_CONFIGURATION