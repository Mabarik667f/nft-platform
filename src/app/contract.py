import web3

from .contracts_data import *

GANACHE_URL = 'HTTP://localhost:7545'
w3 = web3.Web3(web3.HTTPProvider(GANACHE_URL))

# w3.eth.default_account = w3.eth.accounts[0]
# token_contact = w3.eth.contract(bytecode=bytecode_token, abi=abi_token)
# tx_token_hash = token_contact.constructor().transact()
# tx_token_receipt = w3.eth.wait_for_transaction_receipt(tx_token_hash)
# token_address = tx_token_receipt.contractAddress
#
# my_token_contract = w3.eth.contract(bytecode=bytecode_my_token, abi=abi_my_token)
# tx_my_token_hash = my_token_contract.constructor(w3.eth.accounts[0]).transact()
# tx_my_token_receipt = w3.eth.wait_for_transaction_receipt(tx_my_token_hash)
# my_token_address = tx_my_token_receipt.contractAddress
#
# auction_contract = w3.eth.contract(bytecode=bytecode_auction, abi=abi_auction)
# tx_auction_hash = auction_contract.constructor(token_address, my_token_address).transact()
# tx_auction_receipt = w3.eth.wait_for_transaction_receipt(tx_auction_hash)
# auction_address = tx_auction_receipt.contractAddress

contract_address = "0xF7316Fe0A97ed63A853a0f755e0012090d595936"
contract = w3.eth.contract(address=contract_address, abi=abi_auction)
