from telegram.ext import ConversationHandler

(
    SELECT_ADMIN_VIEW, 
    SELECT_USER_VIEW,
    START_OVER,
    STOPPING
) = map(chr,range(0,4))

(
    SET_NICKNAME,
    REMOVE_NICKNAME, 
    TYPING_REPLY, 
    SEND_PHOTO 
) = map(chr,range(100, 104))

(
    SELECT_ADMIN_FEATURES, 
    START_EVENT_TIME, 
    END_EVENT_TIME, 
    ADD_ADMIN, 
    REMOVE_ADMIN, 
    SET_FORM_LINK 
)= map(chr,range(200, 206))

END = ConversationHandler.END