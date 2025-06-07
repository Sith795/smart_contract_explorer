from web3 import Web3
import json
from config import RPC_URL
from threading import Thread
import time

web3 = Web3(Web3.HTTPProvider(RPC_URL))

def monitor_events(address, abi, callback):
    contract = web3.eth.contract(address=Web3.to_checksum_address(address), abi=json.loads(abi))

    def log_loop(event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                callback(event)
            time.sleep(poll_interval)

    for e in contract.events.__dict__.get("_events", []):
        ev = getattr(contract.events, e.event_name)
        event_filter = ev.create_filter(fromBlock="latest")
        worker = Thread(target=log_loop, args=(event_filter, 2), daemon=True)
        worker.start()
