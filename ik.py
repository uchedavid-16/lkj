import requests,json

def token_balance(contract_address, wallet_address):
    api_key = '' 
    response = requests.get('https://api.bscscan.com/api?module=account&action=tokenbalance'
                           f'&contractaddress={contract_address}&address={wallet_address}&tag=latest&apikey={api_key}')
    result = response.json()['result']
    token_balance = int(result) / 10**18
    fbal = "{:,}".format(float(token_balance))
    print(fbal)
    
    if float(fbal) >= float("10000"):
       


token_balance("0x8cde207ca2b469253586aec336f625eb0b82a4cb","0xaf1ba2e580891c747d6c893d1e701ee9c07c941e")