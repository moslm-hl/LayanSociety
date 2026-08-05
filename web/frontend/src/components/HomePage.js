import React from 'react';
import { ArrowRight, BarChart3, Calculator, ShieldCheck, Sparkles, TrendingUp } from 'lucide-react';

function HomePage({ onNavigate, isDarkMode }) {
  const featureCards = [
    {
      title: 'Live economic snapshots',
      description: 'Monitor GDP, inflation, unemployment, and exchange rates from one calm workspace.',
      icon: BarChart3,
      accent: 'from-pink-500/20 to-pink-500/5',
    },
    {
      title: 'Smarter planning tools',
      description: 'Model future costs and compare scenarios with reliable economic indicators.',
      icon: TrendingUp,
      accent: 'from-blue-500/20 to-blue-500/5',
    },
    {
      title: 'Practical decision support',
      description: 'Move from raw data to confident choices with clear, structured insights.',
      icon: ShieldCheck,
      accent: 'from-pink-500/20 to-blue-500/5',
    },
  ];

  return (
    <div className="space-y-6 fade-in">
      <section className={`panel-soft overflow-hidden rounded-[32px] border ${isDarkMode ? 'border-white/10 bg-gradient-to-br from-slate-900/95 via-slate-800/90 to-slate-900/95' : 'border-slate-200 bg-gradient-to-br from-white/95 via-slate-50/90 to-white/95'} p-8 lg:p-10`}>
        <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
          <div>
            <div className={`mb-4 inline-flex items-center gap-2 rounded-full border border-pink-400/20 bg-pink-400/10 px-3 py-1 text-sm ${isDarkMode ? 'text-pink-200' : 'text-pink-700'}`}>
              <Sparkles className="h-4 w-4" />
              A clearer way to understand the economy
            </div>
            <h2 className={`text-4xl font-semibold tracking-tight ${isDarkMode ? 'text-white' : 'text-slate-900'} sm:text-5xl`}>
              Make sense of Tunisia's economic landscape with confidence.
            </h2>
            <p className={`mt-4 max-w-2xl text-lg leading-8 ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>
              LayanSociety brings together inflation, growth, employment, currency, and interest insights in a polished experience built for practical decisions.
            </p>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <button
                onClick={() => onNavigate('dashboard')}
                className={`inline-flex items-center justify-center gap-2 rounded-full px-5 py-3 text-sm font-semibold transition ${isDarkMode ? 'bg-white text-slate-900 hover:bg-slate-200' : 'bg-slate-900 text-white hover:bg-slate-800'}`}
              >
                Open Dashboard
                <ArrowRight className="h-4 w-4" />
              </button>
              <button
                onClick={() => onNavigate('inflation')}
                className={`inline-flex items-center justify-center gap-2 rounded-full border px-5 py-3 text-sm font-semibold transition ${isDarkMode ? 'border-white/15 bg-white/5 text-white hover:bg-white/10' : 'border-slate-300 bg-slate-100 text-slate-900 hover:bg-slate-200'}`}
              >
                Explore calculators
                <Calculator className="h-4 w-4" />
              </button>
            </div>
          </div>

          <div className={`rounded-[28px] border ${isDarkMode ? 'border-white/10 bg-slate-950/60' : 'border-slate-200 bg-white/60'} p-6 shadow-2xl ${isDarkMode ? 'shadow-black/20' : 'shadow-slate-200/20'}`}>
            <div className={`rounded-[24px] border ${isDarkMode ? 'border-white/10 bg-gradient-to-br from-pink-500/15 via-slate-900/80 to-blue-800/70' : 'border-slate-200 bg-gradient-to-br from-pink-500/15 via-white/80 to-blue-800/70'} p-6`}>
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <p className={`text-sm font-semibold uppercase tracking-[0.24em] ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>Economic overview</p>
                  <h3 className={`mt-2 text-xl font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Trusted by planners and analysts</h3>
                </div>
                <div className="rounded-full border border-pink-400/20 bg-pink-500/10 px-3 py-1 text-sm text-pink-300">
                  Updated
                </div>
              </div>

              <div className="space-y-3">
                <div className={`rounded-2xl border ${isDarkMode ? 'border-white/10 bg-slate-950/45' : 'border-slate-200 bg-slate-50'} p-4`}>
                  <div className={`mb-2 flex items-center justify-between text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                    <span>GDP outlook</span>
                    <span className="text-pink-400">Positive</span>
                  </div>
                  <p className={`text-2xl font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>+2.4%</p>
                </div>
                <div className={`rounded-2xl border ${isDarkMode ? 'border-white/10 bg-slate-950/45' : 'border-slate-200 bg-slate-50'} p-4`}>
                  <div className={`mb-2 flex items-center justify-between text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                    <span>Inflation focus</span>
                    <span className="text-blue-400">Watchlist</span>
                  </div>
                  <p className={`text-2xl font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Stable trend</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        {featureCards.map((card) => {
          const Icon = card.icon;
          return (
            <div key={card.title} className={`panel-soft rounded-[24px] border ${isDarkMode ? 'border-white/10' : 'border-slate-200'} bg-gradient-to-br ${card.accent} p-6`}>
              <div className={`mb-4 flex h-12 w-12 items-center justify-center rounded-2xl ${isDarkMode ? 'bg-slate-950/60' : 'bg-slate-100'}`}>
                <Icon className={`h-5 w-5 ${isDarkMode ? 'text-white' : 'text-slate-900'}`} />
              </div>
              <h3 className={`text-xl font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>{card.title}</h3>
              <p className={`mt-2 text-sm leading-6 ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>{card.description}</p>
            </div>
          );
        })}
      </section>

      <section className={`panel-soft rounded-[28px] border ${isDarkMode ? 'border-white/10' : 'border-slate-200'} p-6`}>
        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className={`text-sm font-semibold uppercase tracking-[0.24em] ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>Explore the platform</p>
            <h3 className={`mt-2 text-2xl font-semibold ${isDarkMode ? 'text-white' : 'text-slate-900'}`}>Everything you need to understand the numbers in one place.</h3>
          </div>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => onNavigate('currency')}
              className={`rounded-full border px-4 py-2 text-sm font-medium transition ${isDarkMode ? 'border-white/10 bg-white/5 text-white hover:bg-white/10' : 'border-slate-300 bg-slate-100 text-slate-900 hover:bg-slate-200'}`}
            >
              Currency tools
            </button>
            <button
              onClick={() => onNavigate('interest')}
              className={`rounded-full border px-4 py-2 text-sm font-medium transition ${isDarkMode ? 'border-white/10 bg-white/5 text-white hover:bg-white/10' : 'border-slate-300 bg-slate-100 text-slate-900 hover:bg-slate-200'}`}
            >
              Interest calculator
            </button>
            <button
              onClick={() => onNavigate('gdp')}
              className={`rounded-full border px-4 py-2 text-sm font-medium transition ${isDarkMode ? 'border-white/10 bg-white/5 text-white hover:bg-white/10' : 'border-slate-300 bg-slate-100 text-slate-900 hover:bg-slate-200'}`}
            >
              GDP projection
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
