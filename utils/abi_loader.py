import requests
from config import ETHERSCAN_API_KEY, EXPLORER_API

def get_contract_abi(address):
    params = {
        "module": "contract",
        "action": "getabi",
        "address": address,
        "apikey": ETHERSCAN_API_KEY
    }
    res = requests.get(EXPLORER_API, params=params)
    return res.json()["result"]
