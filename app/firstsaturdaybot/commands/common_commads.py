from firstsaturdaybot.commands import *
from telegram import Update
from telegram.ext import ContextTypes

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = "Sorry, I didn't understand that command."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return END

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Okay, bye.")
    context.user_data.clear()
    return END

async def stop_nested_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Okay, bye.")
    context.user_data.clear()
    return END

async def invalid_button_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕 Please send /start to get a new keyboard."
    )

async def reply_message (conv_type, text, update, context) -> int:
    if conv_type == "message":
        await update.message.reply_text(text)
        context.user_data.clear()
        return END
    elif conv_type == "callback":
        await update.callback_query.answer()
        await update.callback_query.edit_text(text)
        context.user_data.clear()
        return END