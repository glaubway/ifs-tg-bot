from firstsaturdaybot import (
    IFSCONFIGURATION,
    IFSDATABASE,
    IFSEVENTTIME
)
from firstsaturdaybot.commands.common_commads import (
    clear_user_data,
    remove_start_over,
    set_start_over
)
from firstsaturdaybot.handlers.security import restricted_admin
from firstsaturdaybot.handlers.ifsconstants import (
    SELECTING_ADMIN_ACTION,
    SET_START_EVENT_TIME,
    SET_END_EVENT_TIME,
    ADD_ADMIN,
    REMOVE_ADMIN,
    SET_STATISTIC_FORM_LINK,
    SET_PORTAL_HUNT_SPREADSHEET_LINK,
    SET_EVENT_RESTRICTION_POLICY,
    CHANGE_DATE_RESTRICTION,
    CHANGE_TIME_RESTRICTION,
    TYPING_TIME_CONFIGURATION,
    TYPING_STATISTIC_SPREADSHEET_LINK,
    TYPING_PORTAL_HUNT_SPREADSHEET_LINK,
    TYPING_ADD_ADMIN,
    TYPING_REMOVE_ADMIN,
    TYPING_EVENT_RESTRICTION,
    SHOW_CURRENT_CONFIGURATION,
    CURRENT_FEATURE,
    START_OVER,
    STOP_CONVERSATION
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


@restricted_admin
async def admin_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = '') -> str:
    if text == '':
        text = f"Hi {update.effective_user.username}!"
        text += "\nI'm FirstSaturday Bot and I'm here to help you gather information about event participants."
        text += "\nIn this menu, you can easily customize me."
        text += "\nTo abort, simply type /stop."

    keyboard = InlineKeyboardMarkup([
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
    ])

    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=text, 
                                       reply_markup=keyboard)

    remove_start_over(context)

    return SELECTING_ADMIN_ACTION


@restricted_admin
async def set_event_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data[CURRENT_FEATURE] = update.callback_query.data
    text: str

    if update.callback_query.data == str(SET_START_EVENT_TIME):
        text = "Please provide start event time in the next format HH:MM."
    elif update.callback_query.data == str(SET_END_EVENT_TIME):
        text = "Please provide end event time in the next format HH:MM."
    else:
        return await admin_start_command(update, context)

    buttons = [[InlineKeyboardButton(text="Return Back", callback_data=str(SELECTING_ADMIN_ACTION))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    set_start_over(context)

    return TYPING_TIME_CONFIGURATION


@restricted_admin
async def set_event_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data[CURRENT_FEATURE] = update.callback_query.data
    NEXT_STAGE: str
    buttons: list = []
    text: str

    if update.callback_query.data == str(ADD_ADMIN):
        text = "Please provide admin nickname which should be added"
        text += f"\nCurrent admins: {IFSCONFIGURATION.show_current_admins_as_string()}"
        NEXT_STAGE = TYPING_ADD_ADMIN
    elif update.callback_query.data == str(REMOVE_ADMIN):
        text = "Please choose admin nickname which should be removed"
        text += f"\nCurrent admins: {IFSCONFIGURATION.show_current_admins_as_string()}"
        for admin_nickname in IFSCONFIGURATION.show_current_admins_as_list():
            if not IFSCONFIGURATION.is_user_predefined_admin(admin_nickname):
                buttons.append(
                    [InlineKeyboardButton(
                        text=str(admin_nickname),
                        callback_data=str(admin_nickname))]
                )
        NEXT_STAGE = TYPING_REMOVE_ADMIN
    else:
        return await admin_start_command(update, context)

    buttons.append([InlineKeyboardButton(text="Return Back", callback_data=str(SELECTING_ADMIN_ACTION))])
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    set_start_over(context)

    return NEXT_STAGE


@restricted_admin
async def set_event_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data[CURRENT_FEATURE] = update.callback_query.data
    NEXT_STAGE: str
    text: str

    if update.callback_query.data == str(SET_STATISTIC_FORM_LINK):
        text = "Please provide new link to the Google form."
        text += f"\nCurrent link: {IFSCONFIGURATION.STATISTIC_FORM_LINK}"
        NEXT_STAGE = TYPING_STATISTIC_SPREADSHEET_LINK
    elif update.callback_query.data == str(SET_PORTAL_HUNT_SPREADSHEET_LINK):
        text = "Please provide new link to the Portal Hunt spreadsheet."
        text += f"\nCurrent link: {IFSCONFIGURATION.PORTAL_HUNT_SPREADSHEET_LINK}"
        NEXT_STAGE = TYPING_PORTAL_HUNT_SPREADSHEET_LINK
    else:
        return await admin_start_command(update, context)

    buttons = [[InlineKeyboardButton(text="Return Back", callback_data=str(SELECTING_ADMIN_ACTION))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    set_start_over(context)

    return NEXT_STAGE


@restricted_admin
async def set_event_restriction_policy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data[CURRENT_FEATURE] = update.callback_query.data

    text = "There you can change some event restriction policy."
    text += "\nIf you enable time restriction, date restriction will be enabled too."
    text += "\nIf you disable date restriction, time restriction will be disabled too."
    if IFSCONFIGURATION.EVENT_DATE_RESTRICTION:
        buttons = [[InlineKeyboardButton(text="Disable date restriction", callback_data=str(CHANGE_DATE_RESTRICTION))]]
    else:
        buttons = [[InlineKeyboardButton(text="Enable date restriction", callback_data=str(CHANGE_DATE_RESTRICTION))]]

    if IFSCONFIGURATION.EVENT_TIME_RESTRICTION:
        buttons.append([InlineKeyboardButton(text="Disable time restriction", callback_data=str(CHANGE_TIME_RESTRICTION))])
    else:
        buttons.append([InlineKeyboardButton(text="Enable time restriction", callback_data=str(CHANGE_TIME_RESTRICTION))])

    buttons.append([InlineKeyboardButton(text="Return Back", callback_data=str(SELECTING_ADMIN_ACTION))])
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    set_start_over(context)

    return TYPING_EVENT_RESTRICTION


@restricted_admin
async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    username: str = update.message.text
    text: str

    if not IFSCONFIGURATION.is_user_admin(username):
        IFSDATABASE.add_admin(username)
        IFSCONFIGURATION.sync_admins_from_db(IFSDATABASE.show_all_admins())
        text = f"User {username} have been added t admin list."
    else:
        text = f"User {username} is already admin."

    clear_user_data(context)

    return await admin_start_command(update, context, text)


@restricted_admin
async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    username: str = update.callback_query.data
    text: str

    if IFSDATABASE.remove_admin(username):
        IFSCONFIGURATION.sync_admins_from_db(IFSDATABASE.show_all_admins())
        text = f"User {username} has been removed from admin list."
    else:
        text = f"User {username} hasn't been removed."

    clear_user_data(context)

    context.user_data[START_OVER] = True
    return await admin_start_command(update, context, text)


@restricted_admin
async def save_time_configuration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    event_time: str = update.message.text
    text: str

    if context.user_data[CURRENT_FEATURE] == str(SET_START_EVENT_TIME):
        if IFSEVENTTIME.set_start_time(event_time):
            text = f"The new star event time is {event_time}"
        else:
            text = "Start time should be less then end time"
    elif context.user_data[CURRENT_FEATURE] == str(SET_END_EVENT_TIME):
        if IFSEVENTTIME.set_end_time(event_time):
            text = f"The new end event time is {event_time}"
        else:
            text = "End time should be more then start time"

    clear_user_data(context)

    return await admin_start_command(update, context, text)


@restricted_admin
async def save_link_configuration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    event_link: str = update.message.text
    text: str = "The link have been changed."

    if context.user_data[CURRENT_FEATURE] == str(SET_STATISTIC_FORM_LINK):
        IFSCONFIGURATION.set_statistic_form_link(event_link)
    elif context.user_data[CURRENT_FEATURE] == str(SET_PORTAL_HUNT_SPREADSHEET_LINK):
        IFSCONFIGURATION.set_portal_hunt_spreadsheet_link(event_link)

    clear_user_data(context)

    return await admin_start_command(update, context, text)


@restricted_admin
async def change_date_restriction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

    IFSCONFIGURATION.change_date_restriction()

    text: str = "Event date restriction policy have been changed."
    text += f"\nCurrent state {IFSCONFIGURATION.show_date_restriction()}"
    text += f"\nCurrent state {IFSCONFIGURATION.show_time_restriction()}"

    clear_user_data(context)
    set_start_over(context)

    return await admin_start_command(update, context, text)


@restricted_admin
async def change_time_restriction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

    IFSCONFIGURATION.change_time_restriction()

    text: str = "Event time restriction policy have been changed."
    text += f"\nCurrent state {IFSCONFIGURATION.show_date_restriction()}"
    text += f"\nCurrent state {IFSCONFIGURATION.show_time_restriction()}"

    clear_user_data(context)
    set_start_over(context)

    return await admin_start_command(update, context, text)


@restricted_admin
async def show_current_configuration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

    text: str = "The current configuration of the bot is next:"
    text += f"\nStart event time: {IFSEVENTTIME.start_time().strftime('%H:%M %Z')}"
    text += f"\nEnd event time: {IFSEVENTTIME.end_time().strftime('%H:%M %Z')}"
    text += f"\nCurrent timezone: {IFSEVENTTIME.EVENT_TIMEZONE}"
    text += f"\nCurrent city: {IFSCONFIGURATION.EVENT_CITY}"
    text += f"\nAdmins username: {IFSCONFIGURATION.show_current_admins_as_string()}"
    text += f"\n<a href='{IFSCONFIGURATION.STATISTIC_FORM_LINK}'>Google form link</a>"
    text += f"\n<a href='{IFSCONFIGURATION.PORTAL_HUNT_SPREADSHEET_LINK}'>Portal Hunt spreadsheet link</a>"
    text += f"\nEvent date restriction policy: {IFSCONFIGURATION.show_date_restriction()}"
    text += f"\nEvent time restriction policy: {IFSCONFIGURATION.show_time_restriction()}"

    buttons = [[InlineKeyboardButton(text="Return Back", callback_data=str(SELECTING_ADMIN_ACTION))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    set_start_over(context)

    return SHOW_CURRENT_CONFIGURATION
