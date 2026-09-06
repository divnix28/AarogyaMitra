// frontend/src/pages/ChatPage.jsx
import React from 'react';
import ChatWidget from '../components/ChatWidget';

export default function ChatPage() {
  return (
    <div className="text-left max-w-4xl mx-auto">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-slate-800">AI Triage & Chat Assistant</h2>
        <p className="text-sm text-slate-500 mt-1">
          Interactive simulation of the conversational agent utilizing RAG knowledge retrieval and safety guardrails.
        </p>
      </div>
      <ChatWidget />
    </div>
  );
}