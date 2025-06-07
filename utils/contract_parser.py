from web3 import Web3
import json
from config import RPC_URL

web3 = Web3(Web3.HTTPProvider(RPC_URL))

def parse_contract(address, abi):
    contract = web3.eth.contract(address=Web3.to_checksum_address(address), abi=json.loads(abi))
    functions = contract.functions
    events = contract.events
    return functions, events
