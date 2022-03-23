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

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/f75c3200d7374f38a7a9403a7561baaa"))
chain_id = 4
my_Address = "0x1DB4b01C737a737b345A52Da147CcB8d3B3f748E"
private_key = "0x186adefb39ee8f89ecc9cef48a88b99bd800bdf4618372f459d1b1fbbd9f7c12"

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

print(simple_Storage.functions.retrieve().call())

store_transaction = simple_Storage.functions.store(15).buildTransaction({
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_Address,
        "nonce": nonce + 1,
})

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(simple_Storage.functions.retrieve().call())