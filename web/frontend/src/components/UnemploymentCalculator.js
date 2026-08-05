import React, { useState } from 'react';
import { Users, ArrowRight, Download } from 'lucide-react';
import axios from 'axios';

const API_URL = '/api';

function UnemploymentCalculator({ isDarkMode }) {
  const [initialRate, setInitialRate] = useState('');
  const [startYear, setStartYear] = useState('2020');
  const [targetYear, setTargetYear] = useState('2035');
  const [scenario, setScenario] = useState('baseline');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState('');
  const [accountNumber, setAccountNumber] = useState('');

  const calculateUnemployment = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/unemployment`, {
        initial_rate: parseFloat(initialRate),
        start_year: parseInt(startYear),
        target_year: parseInt(targetYear),
        scenario,
      });
      setResult(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error calculating unemployment:', error);
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    if (!result) return;
    try {
      const response = await axios.post(`${API_URL}/api/generate-report`, {
        report_type: 'unemployment',
        data: result,
        username: username || 'Client',
        account_number: accountNumber
      }, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `unemployment_report_${new Date().getTime()}.pdf`);
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
          <Users className="w-8 h-8 text-pink-400" />
          <h2 className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Unemployment Rate Calculator</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Initial Rate (%)</label>
            <input
              type="number"
              step="0.1"
              value={initialRate}
              onChange={(e) => setInitialRate(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
              placeholder="e.g., 15.5"
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
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Target Year</label>
            <select
              value={targetYear}
              onChange={(e) => setTargetYear(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
            >
              {Array.from({ length: 30 }, (_, i) => 2027 + i).map((year) => (
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
          onClick={calculateUnemployment}
          disabled={loading || !initialRate}
          className="mt-6 w-full bg-gradient-to-r from-pink-600 to-blue-800 hover:from-pink-700 hover:to-blue-900 disabled:from-pink-800 disabled:to-blue-950 disabled:cursor-not-allowed text-white font-semibold rounded-xl px-6 py-3 transition-colors duration-200 flex items-center justify-center space-x-2"
        >
          {loading ? (
            'Calculating...'
          ) : (
            <>
              <span>Calculate Unemployment Projection</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>

      {result && (
        <div className="glass rounded-2xl p-6 fade-in">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-white">Unemployment Projection Results</h3>
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
              <p className={`text-gray-500 text-sm ${isDarkMode ? 'text-gray-500' : 'text-slate-400'}`}>Initial Rate</p>
              <p className={`text-xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>{result.initial_rate.toFixed(2)}%</p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-500 text-sm ${isDarkMode ? 'text-gray-500' : 'text-slate-400'}`}>Projected Rate</p>
              <p className={`text-xl font-bold ${result.total_change < 0 ? 'text-green-400' : 'text-red-400'}`}>
                {result.projected_rate.toFixed(2)}%
              </p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-500 text-sm ${isDarkMode ? 'text-gray-500' : 'text-slate-400'}`}>Total Change</p>
              <p className={`text-xl font-bold ${result.total_change < 0 ? 'text-green-400' : 'text-red-400'}`}>
                {result.total_change > 0 ? '+' : ''}{result.total_change.toFixed(2)}%
              </p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-500 text-sm ${isDarkMode ? 'text-gray-500' : 'text-slate-400'}`}>Annual Change</p>
              <p className="text-xl font-bold text-blue-400">{result.annual_change.toFixed(3)}%</p>
            </div>
          </div>

          <div className="bg-white/5 rounded-xl p-4">
            <h4 className={`text-white font-semibold mb-3 ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Year-by-Year Projection</h4>
            <div className="max-h-64 overflow-y-auto space-y-2">
              {Object.entries(result.yearly_projections).map(([year, rate]) => (
                <div key={year} className="flex justify-between items-center p-2 bg-white/5 rounded-lg">
                  <span className="text-gray-400">{year}</span>
                  <span className="text-white font-semibold">{rate.toFixed(2)}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default UnemploymentCalculator;
