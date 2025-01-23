from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# api Keys and Wallet Config
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
TRADING_WALLET_PUBLIC_KEY = os.getenv("TRADING_WALLET_PUBLIC_KEY")
TRADING_WALLET_SECRET_KEY = os.getenv("TRADING_WALLET_SECRET_KEY")

# Constants
SOL_TOKEN_ADDRESS = "So11111111111111111111111111111111111111112"
SOLANA_RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"

# api Config
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")