from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from decimal import Decimal
import logging
from . import log_error
from .config import HOST, PORT
from .trading import (
    fetch_wallet_balances,
    execute_positions_with_jupiter,
    generate_jupiter_quote
)

# Initialize FastAPI app
app = FastAPI(title="Solana Trading Bot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "trading-bot-api"}

@app.get("/api/balance")
async def get_balance():
    try:
        balances = fetch_wallet_balances()
        return {"status": "success", "data": balances}
    except Exception as e:
        log_error(f"Error fetching balance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/quote")
async def get_quote(type: str, token_address: str, amount: float):
    try:
        amount_lamports = int(Decimal(amount) * Decimal(10**9))
        quote = generate_jupiter_quote(type, token_address, amount_lamports)
        return {"status": "success", "data": quote}
    except Exception as e:
        log_error(f"Error generating quote: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/trade")
async def execute_trade(type: str, token_address: str, amount: float):
    try:
        amount_lamports = int(Decimal(amount) * Decimal(10**9))
        
        signature = execute_positions_with_jupiter(
            type,
            token_address,
            amount_lamports
        )
        
        if not signature:
            raise HTTPException(
                status_code=400,
                detail="Trade execution failed"
            )
            
        return {
            "status": "success",
            "data": {
                "signature": signature,
                "explorer_url": f"https://solscan.io/tx/{signature}"
            }
        }
    except Exception as e:
        log_error(f"Error executing trade: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    logging.info(f"Starting server on {HOST}:{PORT}")
    uvicorn.run(
        "api.server:app",
        host=HOST,
        port=PORT,
        reload=True
    )