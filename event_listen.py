from datetime import datetime
import json
from web3 import Web3, HTTPProvider
import asyncio
# import requests
from datetime import datetime
import os
from sql_app.models import Article
from sql_app.database import SessionLocal

# Connect to a local Ethereum node
# w3 = Web3(HTTPProvider('http://172.27.192.1:7545'))
alchemy_url = "https://polygon-mumbai.g.alchemy.com/v2/IEPxbD3EJDjg3i9JrKy0qfuJi5IYoKX6"
w3 = Web3(Web3.HTTPProvider(alchemy_url))
path = os.getcwd()

# Define the contract ABI and address
with open(path + '/contracts/desci/DeSciPrint.json', 'r') as f:
    desci_abi_file = json.load(f)

with open(path + '/contracts/preprint/PrePrintTrack.json', 'r') as f:
    preprint_abi_file = json.load(f)

desci_abi = desci_abi_file['abi']
preprint_abi = preprint_abi_file['abi']


def handle_event(event):
    # print(Web3.to_json(event))
    submitAddress = event.args.submitAddress
    submitTime = event.args.submitTime
    # prevCID = event.args.prevCID
    fileCID = event.args.fileCID
    keyInfo = event.args.keyInfo
    description = event.args.description
    address = event.address

    db_article = Article(cid=fileCID,
                                author_addr=submitAddress,
                                c_status='Pending',
                                descs=description,
                                title=keyInfo,
                                author_info='',
                                abstract='',
                                # submit_time=datetime.fromtimestamp(submitTime).strftime("%Y-%m-%d %H:%M:%S"),
                                submit_time=datetime.fromtimestamp(submitTime),
                                prev_cid='',
                                next_cid='',
                                journal_addr=address)
    
    session = SessionLocal()
    session.add(db_article)
    try:
        session.commit()
        session.refresh(db_article)
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

    print(db_article)

    # response = requests.post('http://127.0.0.1:8000/article/create', data=json.dumps({
    #     'cid': fileCID,
    #     'author_addr': submitAddress,
    #     'c_status': 'Pending',
    #     'descs': description,
    #     'title': keyInfo,
    #     'author_info': '',
    #     'abstract': '',
    #     'submit_time': datetime.fromtimestamp(submitTime).strftime("%Y-%m-%d %H:%M:%S"),
    #     'prev_cid': '',
    #     'next_cid': '',
    #     'journal_addr': address
    # }))
    # print(response)


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)


def create_desci_listeners(loop):
    # loop = asyncio.get_running_loop()
    with open(path + '/contracts/desci/contract-address.json', 'r') as f:
        address_file = json.load(f)

    for obj in address_file:
        address = obj['address']
        contract = w3.eth.contract(address=address, abi=desci_abi)
        submit_event_filter = contract.events.Submit.create_filter(
            fromBlock='latest')
        loop.create_task(log_loop(submit_event_filter, 2))


def create_preprint_listeners(loop):
    # loop = asyncio.get_running_loop()
    with open(path + '/contracts/preprint/contract-address.json', 'r') as f:
        address_file = json.load(f)

    for obj in address_file:
        address = obj['address']
        contract = w3.eth.contract(address=address, abi=preprint_abi)
        submit_event_filter = contract.events.Submit.create_filter(
            fromBlock='latest')
        loop.create_task(log_loop(submit_event_filter, 2))


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    # loop = asyncio.get_running_loop()
    loop = asyncio.new_event_loop()
    print('Listening for events...')
    create_desci_listeners(loop)
    create_preprint_listeners(loop)
    try:
        loop.run_forever()
    except Exception as e:
        print(e)
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == '__main__':
    main()
