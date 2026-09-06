// frontend/src/pages/AIEvaluation.jsx
import React from 'react';

export default function AIEvaluation() {
  // Pulling metrics that match your benchmark JSON outputs
  const evaluationData = {
    totalQuestions: 6,
    gatePassed: true,
    overallAccuracy: 82.4,
    rasa: {
      intentAccuracy: 100.0,
      entityF1: 88.89,
      correctIntents: 6,
      failedEntities: 1
    },
    rag: {
      groundingAccuracy: 85.0,
      conceptRecall: 90.0
    },
    safety: {
      emergencyRecall: 100.0,
      criticalFailures: 0
    }
  };

  return (
    <div className="text-left">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-slate-800">AI System Benchmark & Validation</h2>
        <p className="text-sm text-slate-500 mt-1">
          Automated evaluation metrics verifying system reliability against the $\ge$80% success gate.
        </p>
      </div>

      {/* Top Banner Verdict */}
      <div className={`p-6 rounded-xl border mb-8 flex items-center justify-between ${
        evaluationData.gatePassed ? 'bg-emerald-50 border-emerald-200' : 'bg-red-50 border-red-200'
      }`}>
        <div>
          <span className={`text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full ${
            evaluationData.gatePassed ? 'bg-emerald-200 text-emerald-800' : 'bg-red-200 text-red-800'
          }`}>
            Project Gate Status
          </span>
          <h3 className={`text-xl font-bold mt-2 ${evaluationData.gatePassed ? 'text-emerald-900' : 'text-red-900'}`}>
            {evaluationData.gatePassed ? 'SUCCESS: >=80% Target Achieved' : 'WARNING: Target Not Met'}
          </h3>
          <p className="text-sm text-slate-600 mt-1">
            End-to-end testing verified across {evaluationData.totalQuestions} core health queries.
          </p>
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-500">Overall Accuracy</p>
          <p className={`text-4xl font-extrabold ${evaluationData.gatePassed ? 'text-emerald-700' : 'text-red-700'}`}>
            {evaluationData.overallAccuracy}%
          </p>
        </div>
      </div>

      {/* Component Performance Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Rasa NLU Card */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-base font-semibold text-slate-800 mb-1">Rasa NLU (Comprehension)</h3>
          <p className="text-xs text-slate-400 mb-4">Intent classification & entity extraction</p>
          <div className="space-y-3">
            <div className="flex justify-between items-center text-sm">
              <span className="text-slate-600">Intent Accuracy</span>
              <span className="font-bold text-slate-800">{evaluationData.rasa.intentAccuracy}%</span>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-slate-600">Entity F1 Score</span>
              <span className="font-bold text-slate-800">{evaluationData.rasa.entityF1}%</span>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-slate-600">Extraction Failures</span>
              <span className="font-bold text-red-600">{evaluationData.rasa.failedEntities}</span>
            </div>
          </div>
        </div>

        {/* RAG Retrieval Card */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-base font-semibold text-slate-800 mb-1">RAG (Knowledge Grounding)</h3>
          <p className="text-xs text-slate-400 mb-4">Trusted source retrieval & factuality</p>
          <div className="space-y-3">
            <div className="flex justify-between items-center text-sm">
              <span className="text-slate-600">Grounding Accuracy</span>
              <span className="font-bold text-slate-800">{evaluationData.rag.groundingAccuracy}%</span>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-slate-600">Concept Recall</span>
              <span className="font-bold text-slate-800">{evaluationData.rag.conceptRecall}%</span>
            </div>
          </div>
        </div>

        {/* Safety Card */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-base font-semibold text-slate-800 mb-1">HRRS (Safety & Escalation)</h3>
          <p className="text-xs text-slate-400 mb-4">Emergency triage & conservative routing</p>
          <div className="space-y-3">
            <div className="flex justify-between items-center text-sm">
              <span className="text-slate-600">Emergency Recall</span>
              <span className="font-bold text-slate-800">{evaluationData.safety.emergencyRecall}%</span>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-slate-600">Critical Failures</span>
              <span className="font-bold text-emerald-600">{evaluationData.safety.criticalFailures}</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}