import requests
from limit_order_utils import *


def run_limit_order(token_address,
                    token_name,
                    price_threshold,
                    buy_or_sell_amount,
                    position,
                    web3,
                    exchange_contract,
                    exchange_address,
                    my_wallet_address,
                    limit_order_deadline,
                    config):

    bot_start_time = time.time()
    while time.time() - bot_start_time < limit_order_deadline:  # deadline expressed in seconds

        # keep updating the price of token1 through moralis APIs
        tokenprice_endpoint = "https://deep-index.moralis.io/api/v2/erc20/" + str(token_address) + \
                              "/price?chain=bsc"

        header = {
            "x-api-key": config["moralis_api_key"]
        }

        page = requests.request("GET", tokenprice_endpoint, headers=header)
        if page.status_code == 200:
            dict_page = page.json()
            tokenprice_usd = float(dict_page['usdPrice'])
            print('Token: \t {}\t Address: \t {}\n Token Price: \t {}\n'.format(token_name,
                                                                                token_address,
                                                                                tokenprice_usd))

            if position == 'buy':
                if tokenprice_usd <= float(price_threshold):
                    buy_token(web3,
                              exchange_contract,
                              config["addresses"]['wbnb_bsc'],
                              token_address,
                              my_wallet_address,
                              config,
                              amount_to_buy=buy_or_sell_amount)
            if position == 'sell':
                if tokenprice_usd >= float(price_threshold):
                    sell_token(web3,
                               exchange_contract,
                               exchange_address,
                               token_address,
                               config["addresses"]['wbnb_bsc'],
                               my_wallet_address,
                               token_name,
                               config,
                               amount_to_sell=buy_or_sell_amount)

        time.sleep(3)
