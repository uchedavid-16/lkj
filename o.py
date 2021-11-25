from ethtoken.abi import EIP20_ABI
from web3 import Web3
import time

token_from = "0xea87F0353E37882F69867Aa5c2C303ab778e4eA0"
token_to = "0x1F4b4cdcE9DbA53c717d38CAf6E12a81f80754Ff"


#w3 = Web3(Web3.HTTPProvider(infura_url))


contractAddress = "0xAF5912C6F606195a363291F4c6bC7563D6c370E6"
infura_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
# Fill in your infura API key here
w3 = Web3(Web3.HTTPProvider(infura_url))
print(w3.isConnected())

contract = w3.eth.contract(address=contractAddress, abi=EIP20_ABI)

nonce = w3.eth.getTransactionCount(token_from)  



# Build a transaction that invokes this contract's function, called transfer
token_txn = contract.functions.transfer(
     token_to,
     100*10**9,
 ).buildTransaction({
     'chainId': 97,
     'gas': 210000,
     'gasPrice': w3.toWei('50', 'gwei'),
     'nonce': nonce
     
    
 })


signed_txn = w3.eth.account.signTransaction(token_txn, private_key="7e735ccf8c1ec249329cc4f772d6977ec3759ffd74e1e7f4711a256a0cf92b8d")

tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction) 

trans = w3.toHex(tx_hash)
print(trans)
time.sleep(20)