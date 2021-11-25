from web3 import Web3

import time

#bsc = "https://bsc-dataseed.binance.org/"
bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())

account1 = "0xA6d77F5730423908889a16d32Df5B43A132524c1"
rec = "0x1F4b4cdcE9DbA53c717d38CAf6E12a81f80754Ff"

balance = web3.eth.getBalance(account1)
humanReadable = web3.fromWei(balance, 'ether')
print(humanReadable)


print(rec)
nonce = web3.eth.getTransactionCount(account1)
   
    
tx = {
    'nonce': nonce,
    'chainId': 97,
    'to': web3.toChecksumAddress(rec),
    'value': web3.toWei(0.005, 'ether'),
    'gas': 21000,
    'gasPrice': web3.toWei('50', 'gwei')
}
    
signedTx = web3.eth.account.signTransaction(tx, "0xf618dcd88be34e21abd03f6d713965abbb617f97b4a4a0481bf32fbb99b63bed")
tx_hash = web3.eth.sendRawTransaction(signedTx.rawTransaction)
trans = web3.toHex(tx_hash)
print(trans)
time.sleep(20)