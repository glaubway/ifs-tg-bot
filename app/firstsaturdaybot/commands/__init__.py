from telegram.ext import ConversationHandler

(
    CURRENT_FEATURE,
    INCORRECT_INPUT,
    START_OVER,
    STOP_CONVERSATION,
    TO_START
) = map(chr,range(0,5))

(
    SET_NICKNAME,
    REMOVE_NICKNAME,
    TYPING_REPLY,
    SEND_PHOTO
) = map(chr,range(10, 14))

(
    SELECTING_ADMIN_ACTION,
    START_EVENT_TIME,
    END_EVENT_TIME,
    ADD_ADMIN,
    REMOVE_ADMIN,
    SET_FORM_LINK,
    TYPING_CONFIGURATION,
    SHOW_CURRENT_CONFIGURATION
)= map(chr,range(20, 28))

END = ConversationHandler.END