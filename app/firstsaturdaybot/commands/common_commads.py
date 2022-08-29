from firstsaturdaybot.handlers.ifsconstants import (
    END,
    START_OVER
)
from telegram import Update
from telegram.ext import ContextTypes


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text: str = "Sorry, I didn't understand that command."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return END


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text: str = "Okay, bye."
    text += "\nPlease send /start to get a new keyboard."
    if update.message:
        await update.message.reply_text(text)
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text)

    clear_user_data(context)

    return END


async def invalid_button_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text: str = "Sorry, I could not process this button click 😕"
    text += "\nPlease send /start to get a new keyboard."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    clear_user_data(context)


async def reply_message(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        await update.message.reply_text(text)
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text)

    clear_user_data(context)

    return END


async def incorrect_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text="Incorrect input, try again.")
    remove_start_over(context)


def clear_user_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data:
        context.user_data.clear()


def remove_start_over(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[START_OVER] = False


def set_start_over(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[START_OVER] = True
