import React, { useState, useEffect } from 'react';
import { ArrowUpDown, Wallet } from 'lucide-react';

const TradingInterface = () => {
  const [amount, setAmount] = useState('');
  const [tokenAddress, setTokenAddress] = useState('');
  const [walletBalance, setWalletBalance] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTrade = async (type) => {
    setLoading(true);
    try {
      const tradeAmount = parseFloat(amount) * Math.pow(10, 9);
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
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 py-8 px-4">
      <div className="max-w-md mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-lg">
        {/* Header */}
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-2xl font-bold flex items-center gap-3 text-gray-800 dark:text-white">
            <Wallet className="h-6 w-6" />
            Solana Trading Interface
          </h2>
        </div>

        {/* Form */}
        <div className="p-6 space-y-6">
          {/* Token Address Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Token Address
            </label>
            <input
              type="text"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              placeholder="Enter token address"
              value={tokenAddress}
              onChange={(e) => setTokenAddress(e.target.value)}
            />
          </div>

          {/* Amount Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Amount (SOL)
            </label>
            <input
              type="number"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              placeholder="Enter amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
            />
          </div>

          {/* Balance Display */}
          {walletBalance && (
            <div className="text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
              Balance: {(walletBalance.sol?.amount || 0) / Math.pow(10, 9)} SOL
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-4 pt-4">
            <button 
              onClick={() => handleTrade('BUY')}
              disabled={loading}
              className="flex-1 bg-green-500 hover:bg-green-600 text-white py-3 px-4 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Buy
            </button>
            <button 
              onClick={() => handleTrade('SELL')}
              disabled={loading}
              className="flex-1 bg-red-500 hover:bg-red-600 text-white py-3 px-4 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Sell
            </button>
          </div>

          {/* Loading Indicator */}
          {loading && (
            <div className="flex justify-center pt-4">
              <ArrowUpDown className="animate-spin h-6 w-6 text-blue-500" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TradingInterface;