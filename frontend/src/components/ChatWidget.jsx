// frontend/src/components/ChatWidget.jsx
import React, { useState } from 'react';
import { sendChatMessage } from '../services/chatService';

export default function ChatWidget() {
  const [messages, setMessages] = useState([
    { sender: 'ai', text: 'Namaste! I am your AarogyaMitra AI Assistant. How can I help with your health query today?', source: 'System' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [awaitingLearningCheck, setAwaitingLearningCheck] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input;
    setMessages(prev => [...prev, { sender: 'user', text: userMsg }]);
    setInput('');

    if (awaitingLearningCheck) {
      const wordCount = userMsg.trim().split(/\s+/).length;
      setMessages(prev => [...prev, {
        sender: 'ai',
        text: wordCount >= 3
          ? 'Great, you have understood the main point.'
          : 'Please explain a little more so I can check your understanding.',
        source: 'Teach-Back Feedback'
      }]);
      setAwaitingLearningCheck(false);
      return;
    }

    setLoading(true);

    const response = await sendChatMessage(userMsg);
    const learningCheck = response.isEmergency || response.source === 'System Error'
      ? []
      : [{
          sender: 'ai',
          text: 'Learning check: In your own words, what is one important thing you learned from this answer?',
          source: 'Learning Check'
        }];

    setMessages(prev => [
      ...prev,
      { sender: 'ai', text: response.text, source: response.source, isEmergency: response.isEmergency },
      ...learningCheck
    ]);
    setAwaitingLearningCheck(learningCheck.length > 0);
    setLoading(false);
  };

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm flex flex-col h-[500px] text-left">
      <div className="p-4 bg-slate-900 text-white rounded-t-xl font-semibold flex justify-between items-center">
        <span>AarogyaMitra AI Triage Chatbot</span>
        <span className="text-xs bg-emerald-600 px-2 py-0.5 rounded-full">RAG + Rasa Active</span>
      </div>

      <div className="flex-1 overflow-auto p-4 space-y-4 bg-slate-50">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-lg text-sm ${
              msg.sender === 'user' 
                ? 'bg-primary-600 text-white rounded-br-none' 
                : msg.isEmergency 
                  ? 'bg-red-50 border border-red-300 text-red-900 rounded-bl-none' 
                  : 'bg-white border border-slate-200 text-slate-800 rounded-bl-none'
            }`}>
              <p>{msg.text}</p>
              {msg.source && (
                <p className="text-[10px] mt-1 opacity-70 font-mono">Source: {msg.source}</p>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="text-slate-400 text-xs italic">AI is analyzing query against clinical guidelines...</div>
        )}
      </div>

      <form onSubmit={handleSend} className="p-3 border-t border-slate-200 flex gap-2">
        <input 
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a health question (e.g., 'Child has high fever' or 'Chest pain')..."
          className="flex-1 px-3 py-2 border border-slate-300 rounded-md text-sm focus:outline-none focus:border-primary-500"
        />
        <button type="submit" className="bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-700">
          Send
        </button>
      </form>
    </div>
  );
}