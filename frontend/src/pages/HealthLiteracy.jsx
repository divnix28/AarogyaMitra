// frontend/src/pages/HealthLiteracy.jsx
import React from 'react';

export default function HealthLiteracy() {
  const literacyData = {
    averageScore: 78,
    totalAssessments: 12450,
    topicBreakdown: [
      { topic: "Maternal & Child Health", score: 84, status: "Strong" },
      { topic: "Routine Immunization", score: 79, status: "Good" },
      { topic: "Vector-Borne Disease Prevention", score: 68, status: "Needs Intervention" },
      { topic: "Nutrition & Micronutrients", score: 72, status: "Moderate" }
    ],
    recentInterventions: [
      { id: 1, district: "Block North-4", campaign: "Polio Awareness Drive", impact: "+12% Literacy Gain" },
      { id: 2, district: "Block East-2", campaign: "Anemia Screening Camp", impact: "+8% Literacy Gain" }
    ]
  };

  return (
    <div className="text-left">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-slate-800">Health Literacy Analytics</h2>
        <p className="text-sm text-slate-500 mt-1">
          Tracking citizen comprehension metrics across rural and semi-urban health modules.
        </p>
      </div>

      {/* Top Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-sm font-medium text-slate-500">Global Literacy Index</h3>
          <p className="text-3xl font-bold text-slate-800 mt-2">{literacyData.averageScore}%</p>
          <p className="text-xs text-emerald-600 mt-1">↑ 4.2% higher than last quarter</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-sm font-medium text-slate-500">Evaluated Interactions</h3>
          <p className="text-3xl font-bold text-slate-800 mt-2">{literacyData.totalAssessments.toLocaleString()}</p>
          <p className="text-xs text-slate-400 mt-1">Across all active voice/chat channels</p>
        </div>
      </div>

      {/* Topic Breakdown Table */}
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden mb-8">
        <div className="p-6 border-b border-slate-200">
          <h3 className="text-lg font-bold text-slate-800">Comprehension by Clinical Domain</h3>
        </div>
        <table className="w-full text-left">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-6 py-3 text-sm font-semibold text-slate-600">Health Domain</th>
              <th className="px-6 py-3 text-sm font-semibold text-slate-600">Comprehension Score</th>
              <th className="px-6 py-3 text-sm font-semibold text-slate-600">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {literacyData.topicBreakdown.map((item, i) => (
              <tr key={i}>
                <td className="px-6 py-4 text-slate-800 font-medium">{item.topic}</td>
                <td className="px-6 py-4 text-slate-600 font-mono">{item.score}%</td>
                <td className="px-6 py-4">
                  <span className={`inline-block px-2.5 py-1 text-xs font-semibold rounded-full ${
                    item.status === 'Strong' ? 'bg-emerald-100 text-emerald-800' :
                    item.status === 'Good' ? 'bg-sky-100 text-sky-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {item.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}