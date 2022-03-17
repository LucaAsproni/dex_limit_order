import time
from web3 import Web3


def connect_to_web3(provider="https://bsc-dataseed.binance.org/"):
    web3 = Web3(Web3.HTTPProvider(provider))
    print('Connected to web3:', web3.isConnected())
    return web3


def set_exchange_contract(my_web3,
                          config,
                          router=None,
                          abi=None):
    # defaults to pancakeswap mainnet
    if router is None:
        router = config["addresses"]["pancakeswapv2_router"]
    if abi is None:
        abi = config["abis"]["pancakeswapv2_router"]

    return my_web3.eth.contract(address=router, abi=abi)


def get_exchange_address(config, router=None):
    # defaults to pancakeswap mainnet
    if router is None:
        router = config["addresses"]["pancakeswapv2_router"]

    return router


def get_token_balance(web3, wallet_address, token_name, config):
    try:
        token = web3.eth.contract(address=web3.toChecksumAddress(config["addresses"][token_name]),
                                  abi=config["abis"][token_name])
        token_balance = token.functions.balanceOf(wallet_address).call()
        print('Token: {}\t Balance: {}'.format(token_name, token_balance))

        return token_balance

    except:
        if token_name not in config["abis"].keys():
            print('Token ABI not stored.')
        if token_name not in config["addresses"].keys():
            print('Token address not stored.')


def buy_token(web3,
              exchange_contract,
              eth,
              token,
              buyer_wallet,
              config,
              amount_to_buy=None,
              value_in_wei=False,
              gas=250000,
              gas_price='5',
              tx_deadline=1000):

    if amount_to_buy is None:
        # buy whole balance
        amount_to_buy_tx = get_token_balance(web3, buyer_wallet, eth, config)
    else:
        if value_in_wei:
            amount_to_buy_tx = int(amount_to_buy)
        else:
            amount_to_buy_tx = web3.toWei(float(amount_to_buy), 'ether')

    gas_price_tx = web3.toWei(gas_price, 'gwei')

    exchange_tx = exchange_contract.functions.swapExactETHForTokens(
        0,
        [eth, token],
        buyer_wallet,
        int(time.time()) + tx_deadline
    ).buildTransaction({
        'from': buyer_wallet,
        'value': amount_to_buy_tx,
        'gasPrice': gas_price_tx,
        'nonce': web3.eth.get_transaction_count(buyer_wallet),
    })
    signed_tx = web3.eth.account.sign_transaction(exchange_tx, private_key=config["wallet_private_key"])
    tx_token = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = web3.toHex(tx_token)

    return tx_hash


def sell_token(web3,
               exchange_contract,
               exchange_address,
               token,
               eth,
               seller_wallet,
               token_name,
               config,
               amount_to_sell=None,
               value_in_wei=False,
               gas_price='5',
               tx_deadline=1000):

    if amount_to_sell is None:
        # sell whole balance
        amount_to_sell_tx = get_token_balance(web3, seller_wallet, token_name, config)
    else:
        if value_in_wei:
            amount_to_sell_tx = int(amount_to_sell)
        else:
            amount_to_sell_tx = web3.toWei(float(amount_to_sell), 'ether')

    gas_price_tx = web3.toWei(gas_price, 'gwei')

    # APPROVE
    sell_token_contract = web3.eth.contract(token, abi=config["abis"][token_name])
    balance = sell_token_contract.functions.balanceOf(seller_wallet).call()
    approve = sell_token_contract.functions.approve(exchange_address, balance).buildTransaction({
            'from': seller_wallet,
            'gasPrice': gas_price_tx,
            'nonce': web3.eth.get_transaction_count(seller_wallet),
            })

    signed_txn = web3.eth.account.sign_transaction(approve, private_key=config["wallet_private_key"])
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Approved: " + web3.toHex(tx_token))

    # wait for approve to work
    time.sleep(120)

    exchange_tx = exchange_contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
        amount_to_sell_tx,
        0,
        [token, eth],
        seller_wallet,
        int(time.time()) + tx_deadline
    ).buildTransaction({
        'from': seller_wallet,
        'gasPrice': gas_price_tx,
        'nonce': web3.eth.get_transaction_count(seller_wallet),
    })
    signed_tx = web3.eth.account.sign_transaction(exchange_tx, private_key=config["wallet_private_key"])
    tx_token = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = web3.toHex(tx_token)

    return tx_hash
