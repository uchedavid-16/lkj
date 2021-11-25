import json
import time

from web3 import Web3

import time
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

from telegram.ext import *
from telegram import *
import requests
import cryptonator

#bsc = "https://bsc-dataseed.binance.org/"
bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())


keyee =[["BALANCE 💰"],["📥 DEPOSIT","SEND 📤"],["🟡 LOCKS","ℹ️ Info","Help ☎️"]]
markse = ReplyKeyboardMarkup(keyee,one_time_keyboard=False,resize_keyboard=True)



def price_tsc():
    ca = "0x8cde207ca2b469253586aec336f625eb0b82a4cb"
    dates = "%Y-%m-%d %H:%M:%S"
    query = """
    query
    {
      ethereum(network: bsc) {
        dexTrades(
        exchangeName: {in:["Pancake","Pancake v2"]},
        baseCurrency: {is: "%s"}
        quoteCurrency: {is: "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"}
        options: {desc: ["block.height", "transaction.index"], limit: 1}
        ) {
        block {
            height
            timestamp {
            time(format: "%s")
            }
        }
        transaction {
            index
        }
        baseCurrency {
            symbol
        }
        quoteCurrency {
            symbol
        }
        quotePrice
        
       }
       
      }
    }
    """ % (ca, dates)

    d = {'query': query, 'variables': {}}
    payload = json.dumps(d)
    url = "https://graphql.bitquery.io"
    headers = {
            'X-API-KEY': 'BQYxBh0DXYCwroM9PKnGS2tZXWDZhNEx',
            'Content-Type': 'application/json'
        }
    di = requests.request("POST", url, headers=headers, data=payload).json()['data']['ethereum']['dexTrades']
    print(di)
    # Price of coin in BNB
    price = di[0]['quotePrice']
    # Getting current price of bnb
    bnb = cryptonator.get_exchange_rate("bnb", "usd")
    
    # Geting price of coin in usd
   
    pr_usd = float(price)*float(bnb)
    
    return pr_usd
    













def deposit(update,context):
    id = update.message.chat_id
    user = str(id) 
    nm = json.load(open('./wallet.json', 'r'))
    bsc = nm['bsc'][user]
    dep_text = f"<b>TradeScapeCash (TSC) Deposit</b>\n\n" \
               f"This is the address to deposit <b>TSC</b>\n\n" \
               f"You can only deposit Bep20 token/coins to this address\n\n" \
               f"<code>{bsc}</code>\n\n"
               
    update.message.reply_text(dep_text,reply_markup=markse,parse_mode='html',disable_web_page_preview=True)
    
    
#----------------------- BALANCE CHECKING BNB AND TSC
# Spent money 
spent_already = json.load(open('./spent.json','r'))


tip_bal = json.load(open("./bal.json","r"))

def token_balance(update,context):
    id = update.message.chat_id
    user = str(id)
    
    nm = json.load(open('./wallet.json', 'r'))
    bsc = nm['bsc'][user] 
    
    api_key = 'NQDD6TXH7G3PBESQWPWSXI5YPA63F6PRXT' 
    response = requests.get('https://api.bscscan.com/api?module=account&action=tokenbalance'
                           f'&contractaddress=0x8cde207ca2b469253586aec336f625eb0b82a4cb&address={bsc}&tag=latest&apikey={api_key}')
    result = response.json()['result']
    token_balance = int(result) / 10**18
    
    #TIP BAL
    gift = tip_bal['tipbal'][user]
    chop = spent_already['spent'][user]
    new_bal = float(token_balance)-float(chop)+float(gift)
    fbal = "{:,.6}".format(float(new_bal))
    pp = price_tsc()
    molo = float(new_bal)*float(pp)
    mlko = "${:,.6}".format(float(molo))
    
    account1 = bsc
    bnb = cryptonator.get_exchange_rate("bnb","usd")
    
    balance = web3.eth.getBalance(account1)
    humanReadable = web3.fromWei(balance, 'ether')
    if humanReadable >= 0.005:
        humanReadable = "{:,.5}".format(float(humanReadable))
    else:
        humanReadable = "{:,.9}".format(float(humanReadable))
    
    mk = float(humanReadable)*float(bnb)
    non = "${:,.6}" .format(float(mk))
    print(humanReadable)
    
    
    ms = f"<b>Wallet Balances</b>\n\n" \
         f"<b>TSC:</b> <code>{fbal} ({mlko})</code>\n\n" \
         f"<b>BNB (Bep20):</b> <code>{humanReadable} ({non})</code>"
    
    update.message.reply_text(ms,parse_mode='html',reply_markup=markse,disable_web_page_preview=True)   
    print(ms)
