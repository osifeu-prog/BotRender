import os
from web3 import Web3

def get_w3():
    rpc = os.getenv("BSC_RPC_URL")
    if not rpc:
        raise RuntimeError("BSC_RPC_URL missing")
    return Web3(Web3.HTTPProvider(rpc))

def get_token(w3):
    addr = os.getenv("SELA_TOKEN_ADDRESS")
    if not addr:
        raise RuntimeError("SELA_TOKEN_ADDRESS missing")
    abi = [{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],
            "name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"},
           {"constant":True,"inputs":[{"name":"_owner","type":"address"}],
            "name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]
    return w3.eth.contract(address=Web3.to_checksum_address(addr), abi=abi)

def send_token(to_address: str, amount_wei: int) -> str:
    w3 = get_w3()
    token = get_token(w3)
    pk = os.getenv("TREASURY_PRIVATE_KEY")
    from_addr = os.getenv("TREASURY_ADDRESS")
    if not pk or not from_addr:
        raise RuntimeError("TREASURY_PRIVATE_KEY/TREASURY_ADDRESS missing")
    tx = token.functions.transfer(Web3.to_checksum_address(to_address), amount_wei).build_transaction({
        "from": Web3.to_checksum_address(from_addr),
        "nonce": w3.eth.get_transaction_count(Web3.to_checksum_address(from_addr)),
        "gas": 120000,
        "maxFeePerGas": w3.to_wei("3", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("1", "gwei"),
        "chainId": int(os.getenv("BSC_CHAIN_ID","56")),
    })
    signed = w3.eth.account.sign_transaction(tx, private_key=pk)
    return w3.eth.send_raw_transaction(signed.rawTransaction).hex()
