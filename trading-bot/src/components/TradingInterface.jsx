import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowUpDown, Wallet } from 'lucide-react';

const TradingInterface = () => {
  const [amount, setAmount] = useState('');
  const [tokenAddress, setTokenAddress] = useState('');
  const [walletBalance, setWalletBalance] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTrade = async (type) => {
    setLoading(true);
    try {
      const tradeAmount = parseFloat(amount) * Math.pow(10, 9); // Convert to lamports
      const result = await window.execute_positions_with_jupiter(
        type,
        tokenAddress,
        tradeAmount
      );
      console.log(`Trade ${type} executed:`, result);
    } catch (error) {
      console.error('Trade failed:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    const fetchBalance = async () => {
      try {
        const balances = await window.fetch_wallet_balances();
        setWalletBalance(balances);
      } catch (error) {
        console.error('Failed to fetch balance:', error);
      }
    };
    fetchBalance();
  }, []);

  return (
    <div className="max-w-2xl mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Wallet className="h-6 w-6" />
            Solana Trading Interface
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Token Address</label>
              <Input
                placeholder="Enter token address"
                value={tokenAddress}
                onChange={(e) => setTokenAddress(e.target.value)}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-1">Amount (SOL)</label>
              <Input
                type="number"
                placeholder="Enter amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
              />
            </div>

            {walletBalance && (
              <div className="text-sm">
                Balance: {(walletBalance.sol?.amount || 0) / Math.pow(10, 9)} SOL
              </div>
            )}

            <div className="flex gap-2">
              <Button 
                onClick={() => handleTrade('BUY')}
                disabled={loading}
                className="flex-1"
              >
                Buy
              </Button>
              <Button 
                onClick={() => handleTrade('SELL')}
                disabled={loading}
                className="flex-1"
              >
                Sell
              </Button>
            </div>

            {loading && (
              <div className="flex justify-center">
                <ArrowUpDown className="animate-spin h-6 w-6" />
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default TradingInterface;