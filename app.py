from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

from telegram.ext import *
from telegram import *

import logging
from telegram.constants import CHAT_PRIVATE
from start import start,menu
from deposit import *
from withdraw import *
import telegram

admin = 1185692914
def broadcast(update, context):
    user = update.effective_chat.id
    msg = update.message.text
    msg = msg.replace('/broadcast', '')
    users = json.load(open("./users.json","r"))
    if user == admin: # only if YOU start the command the message will be sent
        try:
            for id in users: # for every user that has start the bot
                msf = f'<b>Global Message</b>\n\n{msg}'
                context.bot.send_message(chat_id=id,text=msf,parse_mode='html',disable_web_page_preview=True)
        except telegram.error.Unauthorized:
            print('User has blocked the bot, so he/she cannot receive messages.')
 
keyee =[["BALANCE 💰"],["📥 DEPOSIT","SEND 📤"],["🟡 LOCKS","ℹ️ Info","Help ☎️"]]
markse = ReplyKeyboardMarkup(keyee,one_time_keyboard=False,resize_keyboard=True)
def restart(update, context):
    id = update.message.chat_id
    user = str(id) 
    tips = json.load(open("./bal.json","r"))
    if user not in tips['tipbal']:
        tips['tipbal'][user] = "0"
        json.dump(tips,open('./bal.json','w'))  
        update.message.reply_text(text="Restarted",parse_mode='html',disable_web_page_preview=True,reply_markup=markse)
    else:
        update.message.reply_text(text="Welcome Back",parse_mode='html',disable_web_page_preview=True,reply_markup=markse)
def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    #token = "2092169769:AAEXjXFgeSt193R334dzuFsvULO4qZDXy3o"
    token =  "2145272869:AAEXETQ3rCJjoMnspaaNgiHfoT1vLRZiJOQ"
    updater = Updater(token)
    #dispatcher = updater
    print('started')
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('deposit',deposit))
    updater.dispatcher.add_handler(CommandHandler('withdraw',send))
    updater.dispatcher.add_handler(CommandHandler('balance', token_balance))
    updater.dispatcher.add_handler(CommandHandler('tip', tip))
    updater.dispatcher.add_handler(CommandHandler('broadcast', broadcast))
    updater.dispatcher.add_handler(CommandHandler('restart', restart))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Register 🟢$'),menu))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^BALANCE 💰$'),token_balance))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^📥 DEPOSIT$'),deposit))
   
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^🟡 LOCKS$'),later))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^ℹ️ Info$'),later))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Help ☎️$'),later))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^SEND 📤$'),sese))
    
   
    
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
    
if __name__ == '__main__':
    main()