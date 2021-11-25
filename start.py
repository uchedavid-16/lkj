from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

from telegram.ext import *
from telegram import *
from web3.auto import w3

import logging
from telegram.constants import CHAT_PRIVATE

import json

key3 =[["Register 🟢"]]
marks = ReplyKeyboardMarkup(key3,one_time_keyboard=True,resize_keyboard=True)

keyee =[["BALANCE 💰"],["📥 DEPOSIT","SEND 📤"],["🟡 LOCKS","ℹ️ Info","Help ☎️"]]
markse = ReplyKeyboardMarkup(keyee,one_time_keyboard=False,resize_keyboard=True)
#----------------------------------------------------------------------------------------

#ADMIN MESSAGES AND COMMANDS
admin = json.load(open('./admin.json','r'))
start_text_private = admin['startmessageprivate']
start_text_group = admin['startmessagegroup']

#----------------------------------------------------------------------

#  USER INFO
member = json.load(open('./users.json','r'))
#------------------------------------------------------------------------

wallet = json.load(open('./wallet.json','r'))
tips = json.load(open('./bal.json','r'))


spent = json.load(open('./spent.json','r'))

#----------------------------------------------------------------------
def start(update,context):
    id = update.message.chat_id
    user = str(id) 
    
    if update.effective_chat.type != CHAT_PRIVATE:
        ms = f"Welcome to <b>TSC</b> TIPBBOT"
        reply_mark = InlineKeyboardMarkup(rkey)
        update.message.reply_text(ms,parse_mode='html',disable_web_page_preview=True)
    else:
        
        if user not in member['user']:
            member['user'].append(user)
            acct = w3.eth.account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')
            address = acct.address
            privatekey = acct.privateKey.hex()
            if user not in wallet['bsc']:
                wallet['bsc'][user] = address
            
            if user not in wallet['pvkey']:
                wallet['pvkey'][user] = privatekey
                    
            if user not in spent['spent']:
                spent['spent'][user] = "0"
                
            if user not in tips['tipbal']:
                tips['tipbal'][user] = "0"
                
            json.dump(member,open('./users.json','w'))
            json.dump(wallet,open('./wallet.json','w'))
            json.dump(spent,open('./spent.json','w'))
            json.dump(tips,open('./bal.json','w'))
            
            up = username.upper()
            normally = f"Hello\n<b>Click the button below to be registered</b>"
            update.message.reply_text(text=normally,parse_mode='html',disable_web_page_preview=True,reply_markup=marks)
        else:
            msg = f'<b>Main Menu</b>'
            update.message.reply_text(msg,reply_markup=markse,parse_mode='html')
                
                
                
def menu(update,context):
    id = update.message.chat_id
    user = str(id) 
    nm = json.load(open('./wallet.json', 'r'))
    bsc = nm['bsc'][user]
    msg = f'<b>Successfully Registered</b>\n<code>{bsc}</code>'
    update.message.reply_text(msg,reply_markup=markse,parse_mode='html',disable_web_page_preview=True)
                
        
