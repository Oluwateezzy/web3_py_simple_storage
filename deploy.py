import json
from solcx import compile_standard, install_solc
from web3 import Web3

install_solc("0.8.9")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage = file.read()

#compile Our Solidity

compile_sol = compile_standard(
    {

        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },

    solc_version="0.8.9",
)

with open("compiled_code.json", "w") as file:
    json.dump(compile_sol, file)

#get bytecode
bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get ABI
abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_Address = "0xFE7A0353b25c204f9124892d080CF36209F7908c"
private_key = "0x387f21ce5ee5181a378c17d72e6bf14d64c9b8021161249577673d5fdcb2636f"

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_Address)

transaction = SimpleStorage.constructor().buildTransaction( {
    "gasPrice": w3.eth.gas_price, 
    "chainId": chain_id, 
    "from": my_Address, 
    "nonce": nonce, 
})


signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

simple_Storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(simple_Storage.functions.retrieve().call(15))