import React, { useState, useEffect } from 'react';
import { Calculator, TrendingUp, Users, DollarSign, Landmark, BarChart3, Home, Sun, Moon } from 'lucide-react';
import './App.css';
import HomePage from './components/HomePage';
import Dashboard from './components/Dashboard';
import InflationCalculator from './components/InflationCalculator';
import GDPCalculator from './components/GDPCalculator';
import UnemploymentCalculator from './components/UnemploymentCalculator';
import CurrencyConverter from './components/CurrencyConverter';
import InterestCalculator from './components/InterestCalculator';

function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [isDarkMode, setIsDarkMode] = useState(true);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setIsDarkMode(savedTheme === 'dark');
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = !isDarkMode;
    setIsDarkMode(newTheme);
    localStorage.setItem('theme', newTheme ? 'dark' : 'light');
  };

  const tabs = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'inflation', label: 'Inflation Calculator', icon: Calculator },
    { id: 'gdp', label: 'GDP Projection', icon: TrendingUp },
    { id: 'unemployment', label: 'Unemployment Rate', icon: Users },
    { id: 'currency', label: 'Currency Converter', icon: DollarSign },
    { id: 'interest', label: 'Interest Calculator', icon: Landmark },
  ];

  return (
    <div className={`min-h-screen ${isDarkMode ? 'bg-[radial-gradient(circle_at_top_left,_rgba(236,72,153,0.18),_transparent_28%),radial-gradient(circle_at_top_right,_rgba(0,51,102,0.20),_transparent_30%),linear-gradient(135deg,_#1a1a2e_0%,_#16213e_45%,_#0f3460_100%)] text-slate-100' : 'bg-gradient-to-br from-pink-50 via-white to-blue-50 text-slate-900'}`}>
      <header className={`border-b ${isDarkMode ? 'border-white/10 bg-slate-950/70' : 'border-slate-200 bg-white/80'} backdrop-blur-xl`}>
        <div className="mx-auto flex max-w-7xl flex-col gap-5 px-4 py-6 lg:flex-row lg:items-center lg:justify-between lg:px-6">
          <div className="flex items-center gap-4">
            <div className={`flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-pink-400 via-pink-500 to-blue-800 shadow-lg ${isDarkMode ? 'shadow-pink-500/20' : 'shadow-pink-500/30'}`}>
              <BarChart3 className="h-6 w-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className={`text-2xl font-semibold tracking-tight ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>LayanSociety</h1>
              </div>
              <p className={`text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>Clear, practical economic guidance for planning and decision-making</p>
            </div>
          </div>

          <button
            onClick={toggleTheme}
            className={`flex h-10 w-10 items-center justify-center rounded-full transition-all duration-200 ${isDarkMode ? 'bg-white/10 text-white hover:bg-white/20' : 'bg-slate-100 text-slate-900 hover:bg-slate-200'}`}
          >
            {isDarkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>
        </div>
      </header>

      <nav className={`border-b ${isDarkMode ? 'border-white/10 bg-slate-950/50' : 'border-slate-200 bg-white/80'} backdrop-blur-xl`}>
        <div className="mx-auto max-w-7xl px-4 py-3 lg:px-6">
          <div className="flex flex-wrap gap-2">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-medium transition-all duration-200 ${
                    activeTab === tab.id
                      ? `border-pink-500/40 bg-gradient-to-r from-pink-600/20 to-blue-800/20 ${isDarkMode ? 'text-white' : 'text-slate-900'} shadow-lg shadow-pink-500/10`
                      : `border-transparent ${isDarkMode ? 'bg-white/5 text-slate-400' : 'bg-slate-100 text-slate-600'} hover:border-pink-500/30 hover:bg-gradient-to-r hover:from-pink-500/10 hover:to-blue-700/10 ${isDarkMode ? 'hover:text-white' : 'hover:text-slate-900'}`
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      <main className="mx-auto max-w-7xl px-4 py-8 lg:px-6">
        {activeTab === 'home' && <HomePage onNavigate={setActiveTab} isDarkMode={isDarkMode} />}
        {activeTab === 'dashboard' && <Dashboard isDarkMode={isDarkMode} />}
        {activeTab === 'inflation' && <InflationCalculator isDarkMode={isDarkMode} />}
        {activeTab === 'gdp' && <GDPCalculator isDarkMode={isDarkMode} />}
        {activeTab === 'unemployment' && <UnemploymentCalculator isDarkMode={isDarkMode} />}
        {activeTab === 'currency' && <CurrencyConverter isDarkMode={isDarkMode} />}
        {activeTab === 'interest' && <InterestCalculator isDarkMode={isDarkMode} />}
      </main>

      <footer className={`mt-12 border-t ${isDarkMode ? 'border-white/10 bg-slate-950/60' : 'border-slate-200 bg-white/80'} backdrop-blur-xl`}>
        <div className="mx-auto max-w-7xl px-4 py-6 lg:px-6">
          <div className="flex flex-col items-center justify-center gap-4 text-center">
            <p className={`text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>© 2026 LayanSociety for Cost Calculation and Risk Estimation</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
