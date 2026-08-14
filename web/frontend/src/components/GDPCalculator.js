import React, { useState } from 'react';
import { TrendingUp, ArrowRight, Download } from 'lucide-react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function GDPCalculator({ isDarkMode }) {
  const [initialGdp, setInitialGdp] = useState('');
  const [startYear, setStartYear] = useState('2020');
  const [targetYear, setTargetYear] = useState('2035');
  const [scenario, setScenario] = useState('baseline');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState('');
  const [accountNumber, setAccountNumber] = useState('');

  const calculateGDP = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/gdp`, {
        initial_gdp: parseFloat(initialGdp),
        start_year: parseInt(startYear),
        target_year: parseInt(targetYear),
        scenario,
      });
      setResult(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error calculating GDP:', error);
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    if (!result) return;
    try {
      const response = await axios.post(`${API_URL}/api/generate-report`, {
        report_type: 'gdp',
        data: result,
        username: username || 'Client',
        account_number: accountNumber
      }, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `gdp_report_${new Date().getTime()}.pdf`);
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
          <TrendingUp className="w-8 h-8 text-pink-400" />
          <h2 className={`text-2xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>GDP Projection Calculator</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div>
            <label className={`block ${isDarkMode ? 'text-gray-400' : 'text-slate-600'} text-sm mb-2`}>Initial GDP (TND)</label>
            <input
              type="number"
              value={initialGdp}
              onChange={(e) => setInitialGdp(e.target.value)}
              className={`w-full ${isDarkMode ? 'bg-white/10 border-white/20 text-white' : 'bg-slate-100 border-slate-300 text-slate-900'} border rounded-xl px-4 py-3 focus:outline-none focus:border-pink-500 transition-colors`}
              placeholder="e.g., 44000000000"
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
          onClick={calculateGDP}
          disabled={loading || !initialGdp}
          className="mt-6 w-full bg-gradient-to-r from-pink-600 to-blue-800 hover:from-pink-700 hover:to-blue-900 disabled:from-pink-800 disabled:to-blue-950 disabled:cursor-not-allowed text-white font-semibold rounded-xl px-6 py-3 transition-colors duration-200 flex items-center justify-center space-x-2"
        >
          {loading ? (
            'Calculating...'
          ) : (
            <>
              <span>Calculate GDP Projection</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>

      {result && (
        <div className="glass rounded-2xl p-6 fade-in">
          <div className="flex items-center justify-between mb-4">
            <h3 className={`text-xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>GDP Projection Results</h3>
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
              <p className={`text-gray-400 text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Initial GDP</p>
              <p className={`text-xl font-bold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>{result.initial_gdp.toLocaleString()} TND</p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-400 text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Projected GDP</p>
              <p className="text-xl font-bold text-blue-400">{result.projected_gdp.toLocaleString(undefined, {maximumFractionDigits: 0})} TND</p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-400 text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Total Growth</p>
              <p className="text-xl font-bold text-pink-400">{result.total_growth_percent.toFixed(2)}%</p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className={`text-gray-400 text-sm mb-1 ${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>Multiplier</p>
              <p className="text-xl font-bold text-blue-300">{(result.projected_gdp / result.initial_gdp).toFixed(2)}x</p>
            </div>
          </div>

          <div className="bg-white/5 rounded-xl p-4">
            <h4 className={`text-white font-semibold mb-3 ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Year-by-Year Projection</h4>
            <div className="max-h-64 overflow-y-auto space-y-2">
              {Object.entries(result.yearly_projections).map(([year, gdp]) => (
                <div key={year} className="flex justify-between items-center p-2 bg-white/5 rounded-lg">
                  <span className={`${isDarkMode ? 'text-gray-400' : 'text-slate-600'}`}>{year}</span>
                  <span className={`text-white font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>{gdp.toLocaleString(undefined, {maximumFractionDigits: 0})} TND</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default GDPCalculator;
