import React, { useState } from 'react';
import { Landmark, ArrowRight, Download } from 'lucide-react';
import axios from 'axios';

const API_URL = '/api';

function InterestCalculator({ isDarkMode }) {
  const [principal, setPrincipal] = useState('');
  const [years, setYears] = useState('');
  const [startYear, setStartYear] = useState('2020');
  const [scenario, setScenario] = useState('baseline');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState('');
  const [accountNumber, setAccountNumber] = useState('');

  const calculateInterest = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/interest`, {
        principal: parseFloat(principal),
        years: parseInt(years),
        start_year: parseInt(startYear),
        scenario,
      });
      setResult(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error calculating interest:', error);
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    if (!result) return;
    try {
      const response = await axios.post(`${API_URL}/api/generate-report`, {
        report_type: 'interest',
        data: result,
        username: username || 'Client',
        account_number: accountNumber
      }, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `interest_report_${new Date().getTime()}.pdf`);
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
          <Landmark className="w-8 h-8 text-pink-400" />
          <h2 className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Interest Rate Impact Calculator</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Principal (TND)</label>
            <input
              type="number"
              value={principal}
              onChange={(e) => setPrincipal(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
              placeholder="e.g., 10000"
            />
          </div>

          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Duration (Years)</label>
            <input
              type="number"
              value={years}
              onChange={(e) => setYears(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
              placeholder="e.g., 5"
            />
          </div>

          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Start Year</label>
            <select
              value={startYear}
              onChange={(e) => setStartYear(e.target.value)}
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
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Scenario</label>
            <select
              value={scenario}
              onChange={(e) => setScenario(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
            >
              <option value="optimistic" className="bg-slate-800">Optimistic</option>
              <option value="baseline" className="bg-slate-800">Baseline</option>
              <option value="pessimistic" className="bg-slate-800">Pessimistic</option>
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
          onClick={calculateInterest}
          disabled={loading || !principal || !years}
          className="mt-6 w-full bg-gradient-to-r from-pink-600 to-blue-800 hover:from-pink-700 hover:to-blue-900 disabled:from-pink-800 disabled:to-blue-950 disabled:cursor-not-allowed text-white font-semibold rounded-xl px-6 py-3 transition-colors duration-200 flex items-center justify-center space-x-2"
        >
          {loading ? (
            'Calculating...'
          ) : (
            <>
              <span>Calculate Interest Impact</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>

      {result && (
        <div className="glass rounded-2xl p-6 fade-in">
          <div className="flex items-center justify-between mb-4">
            <h3 className={`text-xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Interest Impact Results</h3>
            <button
              onClick={downloadReport}
              className="flex items-center space-x-2 bg-gradient-to-r from-pink-600 to-blue-800 hover:from-pink-700 hover:to-blue-900 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <Download className="w-4 h-4" />
              <span>Download Report</span>
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-400 text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Principal</p>
              <p className={`text-xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>{result.principal.toLocaleString()} TND</p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-400 text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Final Amount</p>
              <p className="text-xl font-bold text-blue-400">{result.final_amount.toLocaleString(undefined, {maximumFractionDigits: 2})} TND</p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-400 text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Total Interest</p>
              <p className="text-xl font-bold text-pink-400">{result.total_interest.toLocaleString(undefined, {maximumFractionDigits: 2})} TND</p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-400 text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Interest %</p>
              <p className="text-xl font-bold text-blue-300">{result.interest_percentage.toFixed(2)}%</p>
            </div>
          </div>

          <div className="bg-white/5 rounded-xl p-4">
            <h4 className={`text-white font-semibold mb-3 ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Year-by-Year Breakdown</h4>
            <div className="max-h-64 overflow-y-auto space-y-2">
              {Object.entries(result.yearly_breakdown).map(([year, balance]) => (
                <div key={year} className="flex justify-between items-center p-2 bg-white/5 rounded-lg">
                  <span className={`${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>{year}</span>
                  <span className={`text-white font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>{balance.toLocaleString(undefined, {maximumFractionDigits: 2})} TND</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default InterestCalculator;
