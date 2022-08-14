from firstsaturdaybot import RUNTIME_CONFIG, RUNTIME_TIME
from firstsaturdaybot.commands import *
from firstsaturdaybot.handlers.security import restricted_admin
from firstsaturdaybot.handlers.logger import myLogger
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

logger = myLogger(__name__)

@restricted_admin
async def admin_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, text=None):
    buttons = [
        [
            InlineKeyboardButton(text="Set start event time", callback_data=str(SET_START_EVENT_TIME)),
            InlineKeyboardButton(text="Set end event time", callback_data=str(SET_END_EVENT_TIME)),
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
            InlineKeyboardButton(text="Change event restriction policy", callback_data=str(SET_EVENT_RESTRICTION_POLICY)),
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

    if update.callback_query.data == str(SET_START_EVENT_TIME):
        text = f"Please provide start event time in the next format HH:MM."
    elif update.callback_query.data == str(SET_END_EVENT_TIME):
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
async def set_event_restriction_policy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[START_OVER] = True
    context.user_data[CURRENT_FEATURE] = update.callback_query.data

    text = "There you can change some event restriction policy.\n"
    text += "If you enable time restriction, date restriction will be enabled too.\n"
    text += "If you disable date restriction, time restriction will be disabled too."
    if RUNTIME_CONFIG.EVENT_DATE_RESTRICTION:
        buttons = [[InlineKeyboardButton(text="Disable date restriction", callback_data=str(CHANGE_DATE_RESTRICTION))]]
    else:
        buttons = [[InlineKeyboardButton(text="Enable date restriction", callback_data=str(CHANGE_DATE_RESTRICTION))]]

    if RUNTIME_CONFIG.EVENT_TIME_RESTRICTION:
        buttons.append([InlineKeyboardButton(text="Disable time restriction", callback_data=str(CHANGE_TIME_RESTRICTION))])
    else:
        buttons.append([InlineKeyboardButton(text="Enable time restriction", callback_data=str(CHANGE_TIME_RESTRICTION))])

    buttons.append([InlineKeyboardButton(text="Return Back", callback_data=str(TO_START))])
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return TYPING_EVENT_RESTRICTION

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

    if context.user_data[CURRENT_FEATURE] == str(SET_START_EVENT_TIME):
        if RUNTIME_TIME.set_start_time(user_message):
            text = f"The new star event time is {user_message}"
        else:
            text = f"Start time should be less then end time"
    elif context.user_data[CURRENT_FEATURE] == str(SET_END_EVENT_TIME):
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
async def change_date_restriction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    RUNTIME_CONFIG.change_date_restriction()

    text = "Event date restriction policy have been changed.\n"
    text += f"Current state {RUNTIME_CONFIG.show_date_restriction()}\n"
    text += f"Current state {RUNTIME_CONFIG.show_time_restriction()}"
    
    context.user_data.clear()
    context.user_data[START_OVER] = True
    await admin_start_command(update, context, text)

@restricted_admin
async def change_time_restriction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    RUNTIME_CONFIG.change_time_restriction()

    text = "Event time restriction policy have been changed.\n"
    text += f"Current state {RUNTIME_CONFIG.show_date_restriction()}\n"
    text += f"Current state {RUNTIME_CONFIG.show_time_restriction()}"
    
    context.user_data.clear()
    context.user_data[START_OVER] = True
    await admin_start_command(update, context, text)

@restricted_admin
async def show_current_configuration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data[START_OVER] = True
    
    text = f"The current configuration of the bot is next:\n"
    text += f"Start event time: {RUNTIME_TIME.start_time().strftime('%H:%M %Z')}\n"
    text += f"End event time: {RUNTIME_TIME.end_time().strftime('%H:%M %Z')}\n"
    text += f"Current timezone: {RUNTIME_TIME.EVENT_TIMEZONE}\n"
    text += f"Current city: {RUNTIME_CONFIG.EVENT_CITY}\n"
    text += f"Admins username: {RUNTIME_CONFIG.show_current_admins_as_string()}\n"
    text += f"<a href='{RUNTIME_CONFIG.STATISTIC_FORM_LINK}'>Google form link</a>\n"
    text += f"<a href='{RUNTIME_CONFIG.PORTAL_HUNT_SPREADSHEET_LINK}'>Portal Hunt spreadsheet link</a>\n"
    text += f"Event date restriction policy: {RUNTIME_CONFIG.show_date_restriction()}\n"
    text += f"Event time restriction policy: {RUNTIME_CONFIG.show_time_restriction()}\n"

    buttons = [[InlineKeyboardButton(text="Return Back", callback_data=str(TO_START))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    return SHOW_CURRENT_CONFIGURATION