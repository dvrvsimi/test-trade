import os
import time
import json
import base64
import requests
from solders import message
from helius import BalancesAPI
from solana.rpc.api import Client
from solders.keypair import Keypair
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed
from solders.transaction import VersionedTransaction


HELIUS_API_KEY = os.getenv('HELIUS_API_KEY')
TRADING_WALLET_PUBLIC_KEY = os.getenv('TRADING_WALLET_PUBLIC_KEY')
TRADING_WALLET_SECRET_KEY = os.getenv('TRADING_WALLET_SECRET_KEY')
SOL_TOKEN_ADDRESS = "So11111111111111111111111111111111111111112"
SOLANA_RPC_URL = "https://mainnet.helius-rpc.com/?api-key=" + HELIUS_API_KEY


def fetch_wallet_balances():
    while True:
        try:
            client = BalancesAPI(HELIUS_API_KEY)
            keypair = Keypair.from_base58_string(TRADING_WALLET_SECRET_KEY)
            balances = client.get_balances(str(keypair.pubkey()))
            wallet_balances = {
                "sol": {
                    "amount": int(balances["nativeBalance"]),
                    "decimals": 9
                }
            }
            for t in balances.get("tokens", []):
                wallet_balances[t["mint"]] = {
                    "amount": int(t["amount"]),
                    "decimals": int(t["decimals"]),
                    "token_account": t["tokenAccount"]
                }
            return wallet_balances
        except:
            time.sleep(1)


def generate_jupiter_quote(execution_type, token_address, trade_amount, retries=10):
    try:
        if execution_type == "BUY":
            inputMint, outputMint = SOL_TOKEN_ADDRESS, token_address
        elif execution_type == "SELL":
            inputMint, outputMint = token_address, SOL_TOKEN_ADDRESS
        else:
            return

        payload = {
            "inputMint": inputMint,
            "outputMint": outputMint,
            "amount": int(trade_amount),
            "swapMode": "ExactIn",
            "autoSlippage": "true",
            "onlyDirectRoutes": "true",
            "restrictIntermediateTokens": "true",
            "autoSlippageCollisionUsdValue": 1000
        }
        r = requests.get("https://api.jup.ag/swap/v1/quote", params=payload)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 429:
            time.sleep(1)
        raise Exception(f"Status Code: {r.status_code}\n{r.content}")
    except:
        if retries > 0:
            time.sleep(1)
            return generate_jupiter_quote(execution_type, token_address, trade_amount, retries - 1)
        else:
            return


def generate_jupiter_swap(execution_type, token_address, trade_amount, retries=10):
    try:
        quote_response = generate_jupiter_quote(execution_type, token_address, trade_amount)
        if quote_response is None:
            return {}

        # sleep to avoid Jupiter rate limits
        time.sleep(1.1)

        payload = {
            "userPublicKey": TRADING_WALLET_PUBLIC_KEY,
            "prioritizationFeeLamports": {
                "priorityLevelWithMaxLamports": {
                    "priorityLevel": "veryHigh",
                    "global": True,
                    "maxLamports": 1_000_000
                }
            },
            "dynamicComputeUnitLimit": True,
            "quoteResponse": quote_response
        }
        r = requests.post("https://api.jup.ag/swap/v1/swap", data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 429:
            time.sleep(1)
        raise Exception(f"Status Code: {r.status_code}\n{r.content}")
    except:
        if retries > 0:
            time.sleep(1)
            return generate_jupiter_swap(execution_type, token_address, trade_amount, retries - 1)
        else:
            return {}


def execute_positions_with_jupiter(execution_type, token_address, trade_amount, retries=10):
    if trade_amount == 0:
        return

    try:
        client = Client(SOLANA_RPC_URL)
        keypair = Keypair.from_base58_string(TRADING_WALLET_SECRET_KEY)

        swap_transaction = generate_jupiter_swap(execution_type, token_address, trade_amount)

        transaction = VersionedTransaction.from_bytes(base64.b64decode(swap_transaction["swapTransaction"]))
        signature = keypair.sign_message(message.to_bytes_versioned(transaction.message))
        signed_txn = VersionedTransaction.populate(transaction.message, [signature])
        txn_signature = client.send_raw_transaction(txn=bytes(signed_txn), opts=TxOpts(preflight_commitment=Confirmed))

        return str(txn_signature.value)
    except:
        if retries > 0:
            time.sleep(1)
            return execute_positions_with_jupiter(execution_type, token_address, trade_amount, retries - 1)
        else:
            return


if __name__ == "__main__":
    # buy usage
    # 1e9 means 1,000,000,000 lamports ~ 1 SOL (9 decimals)
    execute_positions_with_jupiter("BUY", "2qEHjDLDLbuBgRYvsxhc5D6uDWAivNFZGan56P1tpump", 1e9)

    # sell usage
    # 1e6 means 1,000,000 lamports ~ 1 PNUT (6 decimals)
    execute_positions_with_jupiter("SELL", "2qEHjDLDLbuBgRYvsxhc5D6uDWAivNFZGan56P1tpump", 1e6)
