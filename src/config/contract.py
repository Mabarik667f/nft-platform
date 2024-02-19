from .settings import w3
from web3 import Web3

bytecode = ""
abi = '''
'''
Web3.eth.default_account = Web3.eth.accounts[0]
App = Web3.eth.contract(bytecode=bytecode, abi=abi)
tx_hash = App.constructor().transact()
tx_recipient = Web3.eth.wait_for_transaction_receipt(transaction_hash=tx_hash)
contract = Web3.eth.contract(address=tx_recipient.contractAddress, abi=abi)
