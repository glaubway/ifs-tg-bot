from firstsaturdaybot.commands import *
from firstsaturdaybot.tools.timemodule import is_firstsaturday
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = "Sorry, I didn't understand that command."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return END

async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="aaaaa")

async def end_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("See you around!")
    return END

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Okay, bye.")
    context.user_data.clear()
    return END

async def stop_nested_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.callback_query.edit_message_text("Okay, bye.")
    context.user_data.clear()
    return END

async def invalid_button_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕 Please send /start to get a new keyboard."
    )