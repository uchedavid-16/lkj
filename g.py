from web3.auto import w3
acct = w3.eth.account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')
address = acct.address
pv = acct.privateKey.hex()
print(address)
print(pv)