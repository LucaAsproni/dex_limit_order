import sys
import json
from limit_order import *

assert len(sys.argv) >= 6, "Wrong number of input parameters"

wallet = sys.argv[1]
price_threshold = float(sys.argv[2])
token_name = sys.argv[3]
# specify whether it's a buy or sell position
position = sys.argv[4]
assert position == 'buy' or position == 'sell', "Either enter a buy or sell position"
# deadline for the limit order to keep refreshing for the new price, expressed in seconds
limit_order_deadline = int(sys.argv[5])

if len(sys.argv) == 7:
    buy_or_sell_amount = sys.argv[6]
else:
    buy_or_sell_amount = None

# load config data
f = open('../../config_data/config.json')
config = json.load(f)

web3 = connect_to_web3()
exchange_contract = set_exchange_contract(web3, config)  # swapping on this exchange - defaults to pancakeswap
exchange_address = get_exchange_address(config)
my_wallet_address = wallet
token_address = web3.toChecksumAddress(config["addresses"][token_name])

run_limit_order(token_address,
                token_name,
                price_threshold,
                buy_or_sell_amount,
                position,
                web3,
                exchange_contract,
                exchange_address,
                my_wallet_address,
                limit_order_deadline,
                config)
