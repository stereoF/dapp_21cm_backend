import json

from web3 import Web3, HTTPProvider
import requests
import time
import datetime

# Connect to a local Ethereum node
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

# Define the contract ABI and address
contract_address = '0xdDCAF39668067e4eABB683545100Ddce20cc6555'
print(w3.isAddress(contract_address))
contract_abi = [
    {"inputs": [{"internalType": "string", "name": "_name", "type": "string"}], "stateMutability": "nonpayable",
     "type": "constructor"}, {"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "uint256", "name": "changeTime", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "oldValue", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "newValue", "type": "uint256"}],
                              "name": "ChangeEditorActLimit", "type": "event"}, {"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "uint256", "name": "_changeTime", "type": "uint256"},
        {"indexed": False, "internalType": "address[]", "name": "_newEditors", "type": "address[]"}],
                                                                                 "name": "ChangeEditors",
                                                                                 "type": "event"}, {"anonymous": False,
                                                                                                    "inputs": [{
                                                                                                        "indexed": True,
                                                                                                        "internalType": "string",
                                                                                                        "name": "_fileCID",
                                                                                                        "type": "string"},
                                                                                                        {
                                                                                                            "indexed": False,
                                                                                                            "internalType": "address",
                                                                                                            "name": "_editor",
                                                                                                            "type": "address"},
                                                                                                        {
                                                                                                            "indexed": True,
                                                                                                            "internalType": "uint256",
                                                                                                            "name": "_changeTime",
                                                                                                            "type": "uint256"}],
                                                                                                    "name": "ChangePaperEditor",
                                                                                                    "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "string", "name": "fileCID", "type": "string"},
                                    {"indexed": True, "internalType": "uint256", "name": "replyTime",
                                     "type": "uint256"},
                                    {"indexed": False, "internalType": "enum DeSciPrint.ProcessStatus",
                                     "name": "status", "type": "uint8"}], "name": "ChangePaperStatus", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "_editor", "type": "address"},
                                    {"indexed": True, "internalType": "uint256", "name": "_changeTime",
                                     "type": "uint256"},
                                    {"indexed": True, "internalType": "string", "name": "_fileCID", "type": "string"},
                                    {"indexed": False, "internalType": "address[]", "name": "_newReviewers",
                                     "type": "address[]"}], "name": "ChangeReviewers", "type": "event"},
    {"anonymous": False,
     "inputs": [{"indexed": True, "internalType": "address", "name": "balanceOwner", "type": "address"},
                {"indexed": False, "internalType": "uint256", "name": "finalAmount", "type": "uint256"},
                {"indexed": True, "internalType": "uint256", "name": "changeTime", "type": "uint256"}],
     "name": "ChangeToken", "type": "event"}, {"anonymous": False, "inputs": [
        {"indexed": False, "internalType": "enum DeSciPrint.ValueType", "name": "valueType", "type": "uint8"},
        {"indexed": True, "internalType": "uint256", "name": "changeTime", "type": "uint256"},
        {"indexed": True, "internalType": "uint256", "name": "index", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "oldAmount", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "newAmount", "type": "uint256"}], "name": "ChangeValue",
                                               "type": "event"}, {"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "commentator", "type": "address"},
        {"indexed": True, "internalType": "uint256", "name": "commentTime", "type": "uint256"},
        {"indexed": True, "internalType": "string", "name": "targetCID", "type": "string"},
        {"indexed": False, "internalType": "string", "name": "commentCID", "type": "string"},
        {"indexed": False, "internalType": "enum DeSciPrint.ReviewerStatus", "name": "status", "type": "uint8"}],
                                                                  "name": "Comment", "type": "event"},
    {"anonymous": False,
     "inputs": [{"indexed": True, "internalType": "uint256", "name": "_changeTime", "type": "uint256"},
                {"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"},
                {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}],
     "name": "OwnershipTransferred", "type": "event"}, {"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "string", "name": "fileCID", "type": "string"},
        {"indexed": True, "internalType": "address", "name": "toCommentator", "type": "address"},
        {"indexed": True, "internalType": "uint256", "name": "replyTime", "type": "uint256"},
        {"indexed": False, "internalType": "string", "name": "replyCID", "type": "string"}], "name": "ReplyComment",
                                                        "type": "event"}, {"anonymous": False, "inputs": [
        {"indexed": False, "internalType": "string", "name": "prevCID", "type": "string"},
        {"indexed": False, "internalType": "string", "name": "fileCID", "type": "string"},
        {"indexed": False, "internalType": "string", "name": "keyInfo", "type": "string"},
        {"indexed": True, "internalType": "address", "name": "submitAddress", "type": "address"},
        {"indexed": True, "internalType": "uint256", "name": "submitTime", "type": "uint256"},
        {"indexed": False, "internalType": "string", "name": "description", "type": "string"},
        {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "Submit",
                                                                           "type": "event"},
    {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "deSciPrintCIDMap",
     "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view",
     "type": "function", "constant": True},
    {"inputs": [], "name": "deSciPrintCnt", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
     "stateMutability": "view", "type": "function", "constant": True},
    {"inputs": [{"internalType": "string", "name": "", "type": "string"}], "name": "deSciPrints",
     "outputs": [{"internalType": "address", "name": "submitAddress", "type": "address"},
                 {"internalType": "uint256", "name": "submitTime", "type": "uint256"},
                 {"internalType": "string", "name": "keyInfo", "type": "string"},
                 {"internalType": "string", "name": "prevCID", "type": "string"},
                 {"internalType": "string", "name": "nextCID", "type": "string"}], "stateMutability": "view",
     "type": "function", "constant": True},
    {"inputs": [{"internalType": "string", "name": "", "type": "string"}], "name": "deSciProcess",
     "outputs": [{"internalType": "uint256", "name": "donate", "type": "uint256"},
                 {"internalType": "address", "name": "editor", "type": "address"},
                 {"internalType": "enum DeSciPrint.ProcessStatus", "name": "processStatus", "type": "uint8"},
                 {"internalType": "uint8", "name": "editorActCnt", "type": "uint8"},
                 {"internalType": "uint256", "name": "donateUsed", "type": "uint256"}], "stateMutability": "view",
     "type": "function", "constant": True}, {"inputs": [{"internalType": "string", "name": "", "type": "string"},
                                                        {"internalType": "address", "name": "", "type": "address"}],
                                             "name": "deSciReviews", "outputs": [
            {"internalType": "string", "name": "comment", "type": "string"},
            {"internalType": "uint256", "name": "commentTime", "type": "uint256"},
            {"internalType": "enum DeSciPrint.ReviewerStatus", "name": "reviewerStatus", "type": "uint8"},
            {"internalType": "string", "name": "reply", "type": "string"},
            {"internalType": "uint256", "name": "replyTime", "type": "uint256"}], "stateMutability": "view",
                                             "type": "function", "constant": True},
    {"inputs": [], "name": "editorActLimit", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
     "stateMutability": "view", "type": "function", "constant": True},
    {"inputs": [], "name": "editors", "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
     "stateMutability": "view", "type": "function", "constant": True},
    {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "gasFee",
     "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view",
     "type": "function", "constant": True},
    {"inputs": [], "name": "isEditor", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
     "stateMutability": "view", "type": "function", "constant": True},
    {"inputs": [], "name": "isOwner", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
     "stateMutability": "view", "type": "function", "constant": True},
    {"inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}],
     "stateMutability": "view", "type": "function", "constant": True},
    {"inputs": [], "name": "owner", "outputs": [{"internalType": "address payable", "name": "", "type": "address"}],
     "stateMutability": "view", "type": "function", "constant": True},
    {"inputs": [{"internalType": "address[]", "name": "editorAddrs", "type": "address[]"}], "name": "pushEditors",
     "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address[]", "name": "editorAddrs", "type": "address[]"}], "name": "removeEditor",
     "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"internalType": "string", "name": "", "type": "string"},
                   {"internalType": "address", "name": "", "type": "address"}], "name": "reviewerIndex",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view",
        "type": "function", "constant": True},
    {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "tokenBalance",
     "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view",
     "type": "function", "constant": True},
    {"inputs": [{"internalType": "address payable", "name": "newOwner", "type": "address"}],
     "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"stateMutability": "payable", "type": "receive", "payable": True}, {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"},
                   {"internalType": "uint8", "name": "index", "type": "uint8"}], "name": "setGasFee", "outputs": [],
        "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"},
                   {"internalType": "uint8", "name": "index", "type": "uint8"}], "name": "setBonusWeight",
        "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "bonusWeight", "outputs": [{"internalType": "uint256[9]", "name": "", "type": "uint256[9]"}],
     "stateMutability": "view", "type": "function", "constant": True},
    {"inputs": [{"internalType": "uint8", "name": "limitCnt", "type": "uint8"}], "name": "setEditorActLimit",
     "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "_startIndex", "type": "uint256"},
                   {"internalType": "uint256", "name": "_endIndex", "type": "uint256"}], "name": "deSciFileCIDs",
        "outputs": [{"internalType": "string[]", "name": "", "type": "string[]"}], "stateMutability": "view",
        "type": "function", "constant": True}, {
        "inputs": [{"internalType": "string", "name": "_fileCID", "type": "string"},
                   {"internalType": "string", "name": "_keyInfo", "type": "string"},
                   {"internalType": "string", "name": "_description", "type": "string"},
                   {"internalType": "uint256", "name": "_amount", "type": "uint256"}], "name": "submitForReview",
        "outputs": [], "stateMutability": "payable", "type": "function", "payable": True}, {
        "inputs": [{"internalType": "enum DeSciPrint.ProcessStatus", "name": "_status", "type": "uint8"},
                   {"internalType": "uint256", "name": "_startIndex", "type": "uint256"},
                   {"internalType": "uint256", "name": "_endIndex", "type": "uint256"}], "name": "printsPool",
        "outputs": [{"internalType": "string[]", "name": "printsPool_", "type": "string[]"}], "stateMutability": "view",
        "type": "function", "constant": True}, {
        "inputs": [{"internalType": "string", "name": "fileCID", "type": "string"},
                   {"internalType": "address[]", "name": "reviewers_", "type": "address[]"}], "name": "reviewerAssign",
        "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "string", "name": "fileCID", "type": "string"}], "name": "getReviewers",
     "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}], "stateMutability": "view",
     "type": "function", "constant": True}, {"inputs": [{"internalType": "string", "name": "fileCID", "type": "string"},
                                                        {"internalType": "string", "name": "comment_",
                                                         "type": "string"}], "name": "editorReject", "outputs": [],
                                             "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"internalType": "string", "name": "fileCID", "type": "string"},
                   {"internalType": "address", "name": "reviewer", "type": "address"}], "name": "_isReviewer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view",
        "type": "function", "constant": True}, {
        "inputs": [{"internalType": "string", "name": "fileCID", "type": "string"},
                   {"internalType": "string", "name": "reviewCID", "type": "string"},
                   {"internalType": "enum DeSciPrint.ReviewerStatus", "name": "status", "type": "uint8"}],
        "name": "reviewPrint", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"internalType": "string", "name": "fileCID", "type": "string"},
                   {"internalType": "address", "name": "reviewer", "type": "address"},
                   {"internalType": "string", "name": "replyCID", "type": "string"}], "name": "replyReviewInfo",
        "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"internalType": "string", "name": "preFileCID", "type": "string"},
                   {"internalType": "string", "name": "_fileCID", "type": "string"},
                   {"internalType": "string", "name": "_keyInfo", "type": "string"},
                   {"internalType": "string", "name": "_description", "type": "string"},
                   {"internalType": "uint256", "name": "_amount", "type": "uint256"}], "name": "replyNew",
        "outputs": [], "stateMutability": "payable", "type": "function", "payable": True}, {
        "inputs": [{"internalType": "string", "name": "fileCID", "type": "string"},
                   {"internalType": "address[]", "name": "_reviewers", "type": "address[]"}], "name": "removeReviewer",
        "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"internalType": "string", "name": "fileCID", "type": "string"},
                   {"internalType": "address", "name": "newEditor", "type": "address"}], "name": "changeEditor",
        "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "totalUserBalance",
                                                                              "outputs": [{"internalType": "uint256",
                                                                                           "name": "total",
                                                                                           "type": "uint256"}],
                                                                              "stateMutability": "view",
                                                                              "type": "function", "constant": True},
    {"inputs": [], "name": "withdrawAvalible", "outputs": [], "stateMutability": "payable", "type": "function",
     "payable": True},
    {"inputs": [], "name": "withdrawToken", "outputs": [], "stateMutability": "payable", "type": "function",
     "payable": True},
    {"inputs": [], "name": "getBalance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
     "stateMutability": "view", "type": "function", "constant": True}]  # Replace with the ABI of your contract

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Get a list of all the events defined in the contract
events = contract.events

sumit_event_filter = events.Submit.createFilter(fromBlock='latest')


# Wait for events to be emitted
# while True:
#     for event in event_filter.get_new_entries():
#         print(event)
#         if event == 'Submit':
#             print('Event1 was emitted with the following data:', event.args)
#             response = requests.get('http://localhost:5000/api')
#         elif event.event == 'ChangeReviewers':
#             print('Event2 was emitted with the following data:', event.args)
#         elif event.event == 'ChangePaperEditor':
#             print('An unknown event was emitted with the following data:', event.args)
from datetime import datetime
def handle_event(event):
    print(event)
    submitAddress = event.args.submitAddress
    submitTime = event.args.submitTime
    prevCID = event.args.prevCID
    fileCID = event.args.fileCID
    keyInfo = event.args.keyInfo
    description = event.args.description
    response = requests.post('http://127.0.0.1:8000/article/create', data=json.dumps({
        'cid': fileCID,
        'author_addr': submitAddress,
        'c_status': 'Pending',
        'descs': description,
        'title': '',
        'author_info': '',
        'abstract': '',
        'submit_time': datetime.fromtimestamp(submitTime).strftime("%Y-%m-%d %H:%M:%S"),
        'prev_cid': '',
        'next_cid': '',
        'journal_addr': '0xdDCAF39668067e4eABB683545100Ddce20cc6555'
    }))
    print(response)


def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)


def main():
    log_loop(sumit_event_filter, 2)


if __name__ == '__main__':
    main()
