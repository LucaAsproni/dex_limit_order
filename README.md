# Limit order bot for Decentralized Exchanges (DEXes)
Bot currently runs on BSC.

The price of the token is updated every 3 seconds according to moralis API, for which it is needed to add the api key in the config json.

The private key of the wallet needs to be added in the config json.

The price threshold must be expressed in dollars ($).

As input argument, specify in the following order:
- Wallet public key,
- Price threshold for the limit order,
- A "token_name" string that identifies the token you want to buy or sell, which needs to be the same string stored in the "addresses" and "abis" fields of the config json,
- The position which must be either "buy" or "sell",
- [Optionally] the amount of tokens in WEI that you want to trade.

Every time you want to trade a new token, you need to add the contract address and the ABI in the config json, as is done for WBNB and the pancakeswap v2 router.


## Further improvements

- Generalize to run on other major blockchains and DEXes
- Wait for tx receipt before between the approval and the sell txs
- Check if approval must be done or the token amount is already approved
- Retrieve ABI of a given contract address automatically instead of asking the user to manually insert it
- Create a GUI to ease the use of the bot