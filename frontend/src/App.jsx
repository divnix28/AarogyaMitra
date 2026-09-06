// frontend/src/App.jsx
import React, { useEffect, useState } from 'react';
import DashboardLayout from './layouts/DashboardLayout';
import { fetchDashboardData } from './services/analyticsService';
import AIEvaluation from './pages/AIEvaluation';
import HealthLiteracy from './pages/HealthLiteracy';
import ChatPage from './pages/ChatPage';
import AshaMobileView from './pages/AshaMobileView';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentView, setCurrentView] = useState('overview');

  useEffect(() => {
    const handleHashChange = () => {
      if (window.location.hash === '#evaluation') {
        setCurrentView('evaluation');
      } else if (window.location.hash === '#literacy') {
        setCurrentView('literacy');
      } else if (window.location.hash === '#chat') {
        setCurrentView('chat');
      } else if (window.location.hash === '#asha') {
        setCurrentView('asha');
      } else {
        setCurrentView('overview');
      }
    };
    window.addEventListener('hashchange', handleHashChange);
    handleHashChange();
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  useEffect(() => {
    fetchDashboardData().then((res) => {
      setData(res);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-full text-slate-500 text-lg">
          Loading Analytics securely...
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      {currentView === 'evaluation' ? (
        <AIEvaluation />
      ) : currentView === 'literacy' ? (
        <HealthLiteracy />
      ) : currentView === 'chat' ? (
        <ChatPage />
      ) : currentView === 'asha' ? (
        <AshaMobileView />
      ) : (
        <div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 text-left">
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <h3 className="text-sm font-medium text-slate-500">Avg Health Literacy Score</h3>
              <p className="text-3xl font-bold text-slate-800 mt-2">{data.healthLiteracy.averageScore}%</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <h3 className="text-sm font-medium text-slate-500">Citizen Interactions</h3>
              <p className="text-3xl font-bold text-slate-800 mt-2">{data.healthLiteracy.totalInteractions.toLocaleString()}</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <h3 className="text-sm font-medium text-slate-500">AI System Benchmark</h3>
              <p className={`text-3xl font-bold mt-2 ${data.aiSystemHealth.gatePassed ? 'text-emerald-600' : 'text-red-600'}`}>
                {data.aiSystemHealth.accuracy}% {data.aiSystemHealth.gatePassed && '✓'}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 text-left">
            <div>
              <h2 className="text-lg font-bold text-slate-800 mb-4">Alerts & Intelligence</h2>
              <div className="space-y-4">
                {data.officialAlerts.map(alert => (
                  <div key={alert.id} className="p-4 bg-red-50 border-l-4 border-alert-red rounded-r-md">
                    <p className="text-xs font-bold tracking-wider text-red-600 uppercase mb-1">Official Health Alert</p>
                    <p className="text-red-900 font-medium">{alert.title}</p>
                  </div>
                ))}
                {data.communitySignals.map(signal => (
                  <div key={signal.id} className="p-4 bg-amber-50 border-l-4 border-signal-amber rounded-r-md">
                    <p className="text-xs font-bold tracking-wider text-amber-700 uppercase mb-1">Community Intelligence Signal</p>
                    <p className="text-amber-900">{signal.title}</p>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h2 className="text-lg font-bold text-slate-800 mb-4">Symptom Trends (Anonymous)</h2>
              <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                  <thead className="bg-slate-50 border-b border-slate-200">
                    <tr>
                      <th className="px-6 py-3 text-sm font-semibold text-slate-600">Symptom</th>
                      <th className="px-6 py-3 text-sm font-semibold text-slate-600">Mentions</th>
                      <th className="px-6 py-3 text-sm font-semibold text-slate-600">Trend</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {data.symptomTrends.map((trend, i) => (
                      <tr key={i}>
                        <td className="px-6 py-4 text-slate-800">{trend.symptom}</td>
                        <td className="px-6 py-4 text-slate-600 font-mono">{trend.count}</td>
                        <td className="px-6 py-4">
                          {trend.trend === 'up' ? (
                            <span className="text-red-500 font-medium text-sm">↑ Increasing</span>
                          ) : (
                            <span className="text-slate-400 font-medium text-sm">→ Stable</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}

export default App;