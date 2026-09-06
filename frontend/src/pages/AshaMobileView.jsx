// frontend/src/pages/AshaMobileView.jsx
import React, { useState } from 'react';

export default function AshaMobileView() {
  const [patientName, setPatientName] = useState('');
  const [symptoms, setSymptoms] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="flex justify-center items-center min-h-[600px] text-left">
      {/* Simulated Mobile Device Frame */}
      <div className="w-[380px] bg-white border-4 border-slate-800 rounded-[40px] shadow-2xl overflow-hidden flex flex-col h-[700px]">
        
        {/* Mobile Status Bar */}
        <div className="bg-slate-900 text-white px-6 py-3 flex justify-between items-center text-xs">
          <span>9:41 AM</span>
          <span className="font-bold tracking-wider">AarogyaMitra ASHA</span>
          <span>5G 📶</span>
        </div>

        {/* App Content */}
        <div className="p-6 flex-1 overflow-y-auto bg-slate-50">
          <div className="mb-6">
            <h2 className="text-xl font-bold text-slate-800">Field Household Visit</h2>
            <p className="text-xs text-slate-500 mt-1">Offline-first triage & symptom logging for ASHA workers.</p>
          </div>

          {submitted ? (
            <div className="bg-emerald-50 border border-emerald-200 p-4 rounded-xl text-center my-auto">
              <p className="text-emerald-800 font-bold text-base">Record Synced Locally!</p>
              <p className="text-xs text-emerald-600 mt-1">Will automatically upload to cloud when network signal is detected.</p>
              <button 
                onClick={() => setSubmitted(false)} 
                className="mt-4 bg-emerald-600 text-white px-4 py-2 rounded-lg text-xs font-semibold"
              >
                Log Another Visit
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Beneficiary Name</label>
                <input 
                  type="text" 
                  value={patientName}
                  onChange={(e) => setPatientName(e.target.value)}
                  placeholder="Enter full name"
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Observed Symptoms / Notes</label>
                <textarea 
                  rows="3"
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  placeholder="e.g., High fever for 2 days, cough"
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white"
                />
              </div>

              <div className="bg-amber-50 border border-amber-200 p-3 rounded-lg">
                <p className="text-[11px] text-amber-800 font-medium">
                  🔒 Encrypted SQLite local storage active. Safe for field usage without internet.
                </p>
              </div>

              <button 
                type="submit" 
                className="w-full bg-primary-600 text-white py-2.5 rounded-lg text-sm font-semibold hover:bg-primary-700 shadow-sm"
              >
                Save & Sync Record
              </button>
            </form>
          )}
        </div>

        {/* Mobile Bottom Bar Indicator */}
        <div className="bg-white py-2 flex justify-center border-t border-slate-100">
          <div className="w-32 h-1 bg-slate-300 rounded-full"></div>
        </div>
      </div>
    </div>
  );
}