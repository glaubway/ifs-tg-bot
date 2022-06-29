from firstsaturdaybot.commands import *
from firstsaturdaybot.tools.timemodule import is_firstsaturday
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

async def user_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"Hi {update.message.from_user.username}!\n"
    if is_firstsaturday():
        text += "Today the First Saturday"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return SELECT_USER_VIEW
    else:
        text += "Event haven't been started yet, please retun to me at the first saturday of month."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return END

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = "Sorry, I didn't understand that command."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    return END

async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="aaaaa")

async def end_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()

    text = "See you around!"
    await update.callback_query.edit_message_text(text=text)

    return END

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Okay, bye.")
    return END

async def stop_nested_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text("Okay, bye.")
    return STOPPING
