import React, { useState } from 'react';
import { Calculator, ArrowRight, Download } from 'lucide-react';
import axios from 'axios';

const API_URL = '/api';

function InflationCalculator({ isDarkMode }) {
  const [amount, setAmount] = useState('');
  const [baseYear, setBaseYear] = useState('2020');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState('');
  const [accountNumber, setAccountNumber] = useState('');

  const calculateInflation = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/inflation`, {
        amount: parseFloat(amount),
        base_year: parseInt(baseYear),
      });
      setResult(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error calculating inflation:', error);
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    if (!result) return;
    try {
      const response = await axios.post(`${API_URL}/api/generate-report`, {
        report_type: 'inflation',
        data: result,
        username: username || 'Client',
        account_number: accountNumber
      }, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `inflation_report_${new Date().getTime()}.pdf`);
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
          <Calculator className="w-8 h-8 text-pink-400" />
          <h2 className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Inflation Calculator</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Amount (TND)</label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
              placeholder="Enter amount"
            />
          </div>

          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Base Year</label>
            <select
              value={baseYear}
              onChange={(e) => setBaseYear(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
            >
              {Array.from({ length: 17 }, (_, i) => 2010 + i).map((year) => (
                <option key={year} value={year} className="bg-slate-800">
                  {year}
                </option>
              ))}
            </select>
          </div>

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
          onClick={calculateInflation}
          disabled={loading || !amount}
          className="mt-6 w-full bg-gradient-to-r from-pink-600 to-blue-800 hover:from-pink-700 hover:to-blue-900 disabled:from-pink-800 disabled:to-blue-950 disabled:cursor-not-allowed text-white font-semibold rounded-xl px-6 py-3 transition-colors duration-200 flex items-center justify-center space-x-2"
        >
          {loading ? (
            'Calculating...'
          ) : (
            <>
              <span>Calculate Inflation</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>

      {result && (
        <div className="glass rounded-2xl p-6 fade-in">
          <div className="flex items-center justify-between mb-4">
            <h3 className={`text-xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Results</h3>
            <button
              onClick={downloadReport}
              className="flex items-center space-x-2 bg-gradient-to-r from-pink-600 to-blue-800 hover:from-pink-700 hover:to-blue-900 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <Download className="w-4 h-4" />
              <span>Download Report</span>
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className={`bg-white/5 rounded-xl p-4 ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>
              <p className={`text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Original Amount</p>
              <p className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>{result.original_amount.toLocaleString()} TND</p>
              <p className={`text-sm ${isDarkMode ? 'text-gray-500' : 'text-slate-400'}`}>{result.base_year}</p>
            </div>
            <div className={`bg-white/5 rounded-xl p-4 ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>
              <p className={`text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Adjusted Amount</p>
              <p className={`text-2xl font-bold ${isDarkMode ? 'text-blue-400' : 'text-blue-600'}`}>{result.adjusted_amount.toLocaleString()} TND</p>
              <p className={`text-sm ${isDarkMode ? 'text-gray-500' : 'text-slate-400'}`}>2026</p>
            </div>
            <div className={`bg-white/5 rounded-xl p-4 ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>
              <p className={`text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Multiplier</p>
              <p className={`text-2xl font-bold ${isDarkMode ? 'text-pink-400' : 'text-pink-600'}`}>{result.multiplier.toFixed(2)}x</p>
              <p className={`text-sm ${isDarkMode ? 'text-gray-500' : 'text-slate-400'}`}>Growth factor</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default InflationCalculator;
