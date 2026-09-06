import React from 'react';

export default function DashboardLayout({ children }) {
  return (
    <div className="min-h-screen bg-slate-50 flex text-left">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col">
        <div className="h-16 flex items-center px-6 bg-slate-950 font-bold text-white text-lg tracking-wide">
          AarogyaMitra PHIX
        </div>
        <nav className="flex-1 py-6 px-4 space-y-2">
          <a href="#" className="block px-4 py-2 hover:bg-slate-800 rounded-md">Overview</a>
          <a href="#literacy" className="block px-4 py-2 hover:bg-slate-800 rounded-md">Health Literacy</a>
          <a href="#evaluation" className="block px-4 py-2 hover:bg-slate-800 rounded-md">AI Evaluation</a>
          <a href="#chat" className="block px-4 py-2 hover:bg-slate-800 rounded-md">AI Chatbot</a>
          <a href="#asha" className="block px-4 py-2 hover:bg-slate-800 rounded-md">ASHA Mobile App</a>
        </nav>
        <div className="p-4 text-xs text-slate-500 border-t border-slate-800">
          Govt. Dashboard v1.0 <br/>
          Secure Anonymized Data
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8">
          <h1 className="text-xl font-semibold text-slate-800">Public Health Intelligence</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm font-medium text-slate-500">Demo Mode Active</span>
            <div className="h-8 w-8 bg-slate-200 rounded-full flex items-center justify-center text-slate-600 font-bold">
              M6
            </div>
          </div>
        </header>
        
        <div className="flex-1 overflow-auto p-8">
          {children}
        </div>
      </main>
    </div>
  );
}