import React, { useState, useEffect } from 'react';
import { TrendingUp, DollarSign, Users, BarChart3 } from 'lucide-react';
import axios from 'axios';

const API_URL = '/api';

function Dashboard({ isDarkMode }) {
  const [economicData, setEconomicData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEconomicData();
  }, []);

  const fetchEconomicData = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/economic-summary/2024`);
      setEconomicData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching economic data:', error);
      setLoading(false);
    }
  };

  const formatMetricValue = (value, suffix = '') => {
    if (value === null || value === undefined || value === '') return '—';
    const numericValue = typeof value === 'number' ? value : Number(value);
    return Number.isFinite(numericValue) ? `${numericValue.toFixed(1)}${suffix}` : value;
  };

  const stats = [
    {
      title: 'GDP Growth',
      value: economicData?.gdp_growth_rate || 0,
      icon: TrendingUp,
      color: 'text-pink-400',
      bgColor: 'bg-pink-500/20',
      trend: '+2.4%',
    },
    {
      title: 'Unemployment',
      value: economicData?.unemployment_rate || 0,
      icon: Users,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/20',
      trend: '-0.5%',
    },
    {
      title: 'Interest Rate',
      value: economicData?.central_bank_rate || 0,
      icon: DollarSign,
      color: 'text-pink-300',
      bgColor: 'bg-pink-400/20',
      trend: '-0.25%',
    },
    {
      title: 'GDP Value',
      value: economicData?.gdp_value || 0,
      icon: BarChart3,
      color: 'text-blue-300',
      bgColor: 'bg-blue-400/20',
      trend: '+4.3%',
    },
  ];

  if (loading) {
    return (
      <div className={`flex min-h-[320px] items-center justify-center rounded-3xl border ${isDarkMode ? 'border-white/10 bg-slate-900/70' : 'border-slate-200 bg-white/70'} p-8`}>
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-2 border-pink-400/30 border-t-pink-400" />
          <p className={`text-lg font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Loading economic dashboard</p>
          <p className={`mt-2 text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>Preparing the latest indicators for Tunisia.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 fade-in">
      <section className={`panel-soft overflow-hidden rounded-[32px] border ${isDarkMode ? 'border-white/10 bg-gradient-to-br from-slate-900/95 via-slate-800/90 to-slate-900/95' : 'border-slate-200 bg-gradient-to-br from-white/95 via-slate-50/90 to-white/95'} p-8`}>
        <div className="flex flex-col gap-6 xl:flex-row xl:items-end xl:justify-between">
          <div className="max-w-2xl">
            <p className={`text-sm font-semibold uppercase tracking-[0.28em] ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>Strategic overview</p>
            <h2 className={`mt-2 text-3xl font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Tunisia economic intelligence</h2>
            <p className={`mt-3 text-sm leading-7 ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>
              A concise executive-style view of the country's key economic signals, designed for quick analysis and confident planning.
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            <div className={`rounded-2xl border ${isDarkMode ? 'border-white/10 bg-white/5 text-slate-300' : 'border-slate-200 bg-slate-50 text-slate-700'} px-4 py-3 text-sm`}>
              <p className={`text-xs uppercase tracking-[0.24em] ${isDarkMode ? 'text-slate-500' : 'text-slate-400'}`}>Status</p>
              <p className={`mt-1 font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Live data feed</p>
            </div>
            <div className={`rounded-2xl border ${isDarkMode ? 'border-white/10 bg-white/5 text-slate-300' : 'border-slate-200 bg-slate-50 text-slate-700'} px-4 py-3 text-sm`}>
              <p className={`text-xs uppercase tracking-[0.24em] ${isDarkMode ? 'text-slate-500' : 'text-slate-400'}`}>Reference</p>
              <p className={`mt-1 font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>2024 / Q4</p>
            </div>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className={`panel-soft panel-hover rounded-[24px] border ${isDarkMode ? 'border-white/10' : 'border-slate-200'} p-5`}>
              <div className="mb-4 flex items-start justify-between">
                <div className={`${stat.bgColor} rounded-2xl p-3`}>
                  <Icon className={`h-5 w-5 ${stat.color}`} />
                </div>
                <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${stat.trend.startsWith('+') ? 'text-emerald-400' : 'text-amber-400'}`}>
                  {stat.trend}
                </span>
              </div>
              <h3 className={`mb-2 text-sm font-medium ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>{stat.title}</h3>
              <p className={`text-2xl font-semibold ${stat.color}`}>
                {formatMetricValue(stat.value, stat.title === 'GDP Value' ? '' : '%')}
              </p>
            </div>
          );
        })}
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div className={`panel-soft rounded-[28px] border ${isDarkMode ? 'border-white/10' : 'border-slate-200'} p-6`}>
          <div className="mb-6 flex items-center justify-between">
            <div>
              <p className={`text-xs font-semibold uppercase tracking-[0.24em] ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>Performance snapshot</p>
              <h3 className={`mt-1 text-xl font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Economic balance at a glance</h3>
            </div>
            <div className="rounded-full border border-pink-400/20 bg-pink-500/10 px-3 py-1 text-sm text-pink-300">
              Stable outlook
            </div>
          </div>

          <div className="space-y-4">
            <div className={`rounded-[22px] border ${isDarkMode ? 'border-white/10 bg-slate-950/45' : 'border-slate-200 bg-slate-50'} p-4`}>
              <div className="mb-3 flex items-center justify-between">
                <span className={`text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>GDP growth</span>
                <span className="text-sm font-semibold text-pink-400">{formatMetricValue(economicData?.gdp_growth_rate, '%')}</span>
              </div>
              <div className="h-2 rounded-full bg-slate-800">
                <div className="h-2 w-[74%] rounded-full bg-gradient-to-r from-pink-400 to-blue-600" />
              </div>
            </div>

            <div className={`rounded-[22px] border ${isDarkMode ? 'border-white/10 bg-slate-950/45' : 'border-slate-200 bg-slate-50'} p-4`}>
              <div className="mb-3 flex items-center justify-between">
                <span className={`text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>Inflation pressure</span>
                <span className="text-sm font-semibold text-blue-400">{formatMetricValue(economicData?.central_bank_rate, '%')}</span>
              </div>
              <div className="h-2 rounded-full bg-slate-800">
                <div className="h-2 w-[62%] rounded-full bg-gradient-to-r from-blue-400 to-pink-600" />
              </div>
            </div>

            <div className={`rounded-[22px] border ${isDarkMode ? 'border-white/10 bg-slate-950/45' : 'border-slate-200 bg-slate-50'} p-4`}>
              <div className="mb-3 flex items-center justify-between">
                <span className={`text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>Employment pressure</span>
                <span className="text-sm font-semibold text-pink-300">{formatMetricValue(economicData?.unemployment_rate, '%')}</span>
              </div>
              <div className="h-2 rounded-full bg-slate-800">
                <div className="h-2 w-[40%] rounded-full bg-gradient-to-r from-pink-400 to-blue-600" />
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className={`panel-soft rounded-[28px] border border-pink-400/10 bg-gradient-to-br from-pink-500/10 ${isDarkMode ? 'via-slate-900/95 to-slate-800/90' : 'via-white/95 to-slate-50/90'} p-6`}>
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-pink-300/80">Currency overview</p>
                <h3 className={`mt-1 text-xl font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Exchange rates</h3>
              </div>
              <div className="rounded-full border border-pink-400/20 bg-pink-500/10 px-3 py-1 text-sm text-pink-300">
                Live
              </div>
            </div>

            <div className="space-y-3">
              <div className={`rounded-[22px] border border-pink-400/15 bg-gradient-to-br from-pink-500/15 to-transparent p-4`}>
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-sm font-medium text-pink-300">TND/USD</span>
                  <span className="text-xs uppercase tracking-[0.2em] text-pink-200">USD</span>
                </div>
                <p className={`text-2xl font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>{economicData?.exchange_rate_usd?.toFixed(4) || '3.0800'}</p>
              </div>

              <div className={`rounded-[22px] border border-blue-400/15 bg-gradient-to-br from-blue-500/15 to-transparent p-4`}>
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-sm font-medium text-blue-300">TND/EUR</span>
                  <span className="text-xs uppercase tracking-[0.2em] text-blue-200">EUR</span>
                </div>
                <p className={`text-2xl font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>{economicData?.exchange_rate_eur?.toFixed(4) || '3.3400'}</p>
              </div>
            </div>
          </div>

          <div className={`panel-soft rounded-[28px] border ${isDarkMode ? 'border-white/10' : 'border-slate-200'} p-6`}>
            <p className={`text-xs font-semibold uppercase tracking-[0.24em] ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>Planning context</p>
            <h3 className={`mt-2 text-xl font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Policy environment</h3>
            <p className={`mt-3 text-sm leading-7 ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>
              Central bank decisions continue to influence financing conditions for businesses, households, and investment planning.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
