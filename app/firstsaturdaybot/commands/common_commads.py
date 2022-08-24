from firstsaturdaybot.commands import *
from telegram import Update
from telegram.ext import ContextTypes

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.effective_chat is not None
    text: str = "Sorry, I didn't understand that command."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return END

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Okay, bye.")
    if context.user_data: 
        context.user_data.clear()
    return END

async def stop_nested_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Okay, bye.")
    if context.user_data: 
        context.user_data.clear()
    return END

async def invalid_button_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text: str = "Sorry, I could not process this button click 😕\n"
    text += "Please send /start to get a new keyboard."
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)

async def reply_message (conv_type: str, text: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if conv_type == "message":
        await update.message.reply_text(text)
    elif conv_type == "callback":
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text)
    if context.user_data: 
        context.user_data.clear()
    return END