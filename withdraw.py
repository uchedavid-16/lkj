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
from ethtoken.abi import EIP20_ABI
from web3 import Web3
import time
from telegram.constants import CHAT_PRIVATE

spent_already = json.load(open('./spent.json','r'))
tip_bal = json.load(open("./bal.json","r"))

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())

keyee =[["BALANCE 💰"],["📥 DEPOSIT","SEND 📤"],["🟡 LOCKS","ℹ️ Info","Help ☎️"]]
markse = ReplyKeyboardMarkup(keyee,one_time_keyboard=False,resize_keyboard=True)

member = json.load(open('./users.json','r'))
def tsc_bal(id):
    user = str(id)
    nm = json.load(open('./wallet.json', 'r'))
    bsc = nm['bsc'][user] 
    api_key = 'NQDD6TXH7G3PBESQWPWSXI5YPA63F6PRXT' 
    response = requests.get('https://api.bscscan.com/api?module=account&action=tokenbalance'
                           f'&contractaddress=0x8cde207ca2b469253586aec336f625eb0b82a4cb&address={bsc}&tag=latest&apikey={api_key}')
    result = response.json()['result']
    token_balance = int(result) / 10**18
    
    new_bal = float(token_balance)-float(spent_already['spent'][user])+float(tip_bal['tipbal'][user])
    return new_bal
    
    
def bnb_bal(id):
    user = str(id)
    nm = json.load(open('./wallet.json', 'r'))
    bsc = nm['bsc'][user]
    
    account1 = bsc
   

    balance = web3.eth.getBalance(account1)
    humanReadable = web3.fromWei(balance, 'ether')
    
    return humanReadable
    
def send(update, context):
    id = update.message.chat_id
    user = str(id)
    text = update.message.text.split()
    print(len(text))
    if len(text) ==3:
        tsc = text[1]
        address = text[2]
        print (tsc, address)
        
        try:
            nb = float(tsc)
            bal_tsc = tsc_bal(id)
            bal_bnb = bnb_bal(id)
            
            if float(nb) < float("10"):
                update.message.reply_text("Minimum Withdraw (10,000 <b>TSC</b>)",reply_markup=markse,parse_mode='html',disable_web_page_preview=True)
                return
            if float(nb) > float(bal_tsc):
                update.message.reply_text("Insufficient Balance\nPlease topup",reply_markup=markse,parse_mode='html',disable_web_page_preview=True)
                return
            if float(bal_bnb) < float("0.002"):
                update.message.reply_text("For successful withdrawal, you must have upto 0.002 bnb to complete transactions",reply_markup=markse,parse_mode='html',disable_web_page_preview=True)
                return
            nmg = json.load(open('./wallet.json', 'r'))
    
            w3 = Web3(Web3.HTTPProvider(bsc))
            print(w3.isConnected())
            token_from =  nmg['bsc'][user]
            token_to = address
            contractAddress = "0x8Cde207Ca2b469253586aEC336f625EB0b82a4cB"
            contract = w3.eth.contract(address=contractAddress, abi=EIP20_ABI)

            nonce = w3.eth.getTransactionCount(token_from) 
            token_txn = contract.functions.transfer(
               token_to,
                int(float(tsc))*10**18,
            ).buildTransaction({
                'chainId': 56,
                'gas': 173751,
                'gasPrice': w3.toWei('10', 'gwei'),
                'nonce': nonce
            })
            signed_txn = w3.eth.account.signTransaction(token_txn, private_key=f"{nmg['pvkey'][user]}")
            tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction) 
            trans = w3.toHex(tx_hash)
            print(trans)
            update.message.reply_text(f"Successfully Sent \nhttps://bscscan.com/tx/{trans}",reply_markup=markse,parse_mode='html',disable_web_page_preview=True)
        
            time.sleep(20)
            return
        except ValueError:
            update.message.reply_text("There was an error\nReasons: either gas price is high or you didn't get the correct format for withdraw",parse_mode='html',reply_markup=markse)
        
            
    else:
        
        update.message.reply_text("Command Usage\n/withdraw [amount] [address]",reply_markup=markse,parse_mode='html',disable_web_page_preview=True)
            

def later(update,context):
    update.message.reply_text("Coming Soon...",parse_mode="html",reply_markup=markse)
    
    
def sese(update,context):
    update.message.reply_text("Tips for withdraw\nMake sure you're submiting correct wallet address\nFund your wallet with <b>TSC</b> and <b>BNB (Bep20)</b>\nUse format\n/withdraw [amount] [wallet address]",parse_mode="html",reply_markup=markse)
    
    
    
    
    
    
    
def tip(update,context):
    id = update.message.from_user.id    
    user = str(id)
    
    text = update.message.text.split()
    reply_to_message = update.message.reply_to_message
    
    selolo = json.load(open('./bal.json','r'))
    if update.effective_chat.type == CHAT_PRIVATE:
        update.message.reply_text('can be used only in groups')
        return
    
    if reply_to_message:
        if len(text)==2:
            amount = text[1]
            try:
                number = float(amount)
                nuko = tsc_bal(id)
                user_receiving_gift = reply_to_message.from_user.id
                gifto = str(user_receiving_gift)
                if float(number) > float(nuko):
                    update.message.reply_text("Balance low",parse_mode="html")
                    return
                try:
                    viki = float(selolo['tipbal'][gifto])+float(number)
                    selolo['tipbal'][gifto] = float(viki)
                
                    vhb = float(spent_already['spent'][user])+float(number)  
                    spent_already['spent'][user] = float(vhb)
                    mhn = f"{user} tipped {number} TSC to {gifto}"
                    update.message.reply_text(mhn,parse_mode="html")
                    json.dump(selolo,open('./bal.json','w'))
                    json.dump(spent_already,open('./spent.json','w'))
                except KeyError:
                    update.message.reply_text("User not registered",parse_mode="html")
                
                
                
            except ValueError:
                update.message.reply_text("Second [arg] must be digit",parse_mode="html")
        
        else:
            kk = "Tipping Usage\n" \
                 "Reply a user message with the amount of tsc to tip\n" \
                 "/tip [amount]\n" \
                 "/tip 200"
            update.message.reply_text(kk,parse_mode="html")
        
    else:
        kk = "Tipping Usage\n" \
             "Reply a user message with the amount of tsc to tip\n" \
             "/tip [amount]\n" \
             "/tip 200"
        update.message.reply_text(kk,parse_mode="html")
        