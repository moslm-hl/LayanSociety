import React, { useState } from 'react';
import { DollarSign, ArrowRight, Download } from 'lucide-react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function CurrencyConverter({ isDarkMode }) {
  const [amount, setAmount] = useState('');
  const [fromCurrency, setFromCurrency] = useState('USD');
  const [toCurrency, setToCurrency] = useState('TND');
  const [year, setYear] = useState('2024');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState('');
  const [accountNumber, setAccountNumber] = useState('');

  const convertCurrency = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/currency`, {
        amount: parseFloat(amount),
        from_currency: fromCurrency,
        to_currency: toCurrency,
        year: parseInt(year),
      });
      setResult(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error converting currency:', error);
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    if (!result) return;
    try {
      const response = await axios.post(`${API_URL}/api/generate-report`, {
        report_type: 'currency',
        data: result,
        username: username || 'Client',
        account_number: accountNumber
      }, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `currency_report_${new Date().getTime()}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error generating report:', error);
    }
  };

  return (
    <div className="space-y-6 fade-in">
      <div className="glass rounded-2xl p-8">
        <div className="flex items-center space-x-3 mb-6">
          <DollarSign className="w-8 h-8 text-pink-400" />
          <h2 className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Currency Converter</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Amount</label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
              placeholder="Enter amount"
            />
          </div>

          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>From Currency</label>
            <select
              value={fromCurrency}
              onChange={(e) => setFromCurrency(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
            >
              <option value="TND" className="bg-slate-800">TND - Tunisian Dinar</option>
              <option value="USD" className="bg-slate-800">USD - US Dollar</option>
              <option value="EUR" className="bg-slate-800">EUR - Euro</option>
            </select>
          </div>

          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>To Currency</label>
            <select
              value={toCurrency}
              onChange={(e) => setToCurrency(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
            >
              <option value="TND" className="bg-slate-800">TND - Tunisian Dinar</option>
              <option value="USD" className="bg-slate-800">USD - US Dollar</option>
              <option value="EUR" className="bg-slate-800">EUR - Euro</option>
            </select>
          </div>

          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Year</label>
            <select
              value={year}
              onChange={(e) => setYear(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
            >
              {Array.from({ length: 17 }, (_, i) => 2010 + i).map((y) => (
                <option key={y} value={y} className="bg-slate-800">
                  {y}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Your Name (for report)</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
              placeholder="Enter your name"
            />
          </div>

          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Account Number (optional)</label>
            <input
              type="text"
              value={accountNumber}
              onChange={(e) => setAccountNumber(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
              placeholder="Enter account number"
            />
          </div>
        </div>

        <button
          onClick={convertCurrency}
          disabled={loading || !amount}
          className="mt-6 w-full bg-gradient-to-r from-pink-600 to-blue-800 hover:from-pink-700 hover:to-blue-900 disabled:from-pink-800 disabled:to-blue-950 disabled:cursor-not-allowed text-white font-semibold rounded-xl px-6 py-3 transition-colors duration-200 flex items-center justify-center space-x-2"
        >
          {loading ? (
            'Converting...'
          ) : (
            <>
              <span>Convert Currency</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>

      {result && (
        <div className="glass rounded-2xl p-6 fade-in">
          <div className="flex items-center justify-between mb-4">
            <h3 className={`text-xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Conversion Result</h3>
            <button
              onClick={downloadReport}
              className="flex items-center space-x-2 bg-gradient-to-r from-pink-600 to-blue-800 hover:from-pink-700 hover:to-blue-900 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <Download className="w-4 h-4" />
              <span>Download Report</span>
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-400 text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Original Amount</p>
              <p className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>{result.amount.toLocaleString()} {result.from_currency}</p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-400 text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Converted Amount</p>
              <p className="text-2xl font-bold text-blue-400">{result.converted_amount.toLocaleString(undefined, {maximumFractionDigits: 2})} {result.to_currency}</p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-400 text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Exchange Rate</p>
              <p className="text-2xl font-bold text-pink-400">{result.exchange_rate.toFixed(4)}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CurrencyConverter;
