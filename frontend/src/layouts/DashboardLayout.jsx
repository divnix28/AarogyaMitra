import React, { useState } from 'react';

export default function DashboardLayout({ children }) {
  const [profileOpen, setProfileOpen] = useState(false);
  const [signupOpen, setSignupOpen] = useState(false);
  const [user, setUser] = useState(() => {
    const savedUser = window.localStorage.getItem('aarogyamitra_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const [signupForm, setSignupForm] = useState({ name: '', email: '', role: 'Health Officer', password: '' });
  const [signupError, setSignupError] = useState('');

  const displayName = user?.name || 'M6 Health Officer';
  const initials = displayName
    .split(' ')
    .map(part => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();

  const handleSignup = (event) => {
    event.preventDefault();
    if (signupForm.password.length < 6) {
      setSignupError('Password must be at least 6 characters.');
      return;
    }

    const newUser = {
      name: signupForm.name.trim(),
      email: signupForm.email.trim(),
      role: signupForm.role
    };
    window.localStorage.setItem('aarogyamitra_user', JSON.stringify(newUser));
    setUser(newUser);
    setSignupForm({ name: '', email: '', role: 'Health Officer', password: '' });
    setSignupError('');
    setSignupOpen(false);
    setProfileOpen(true);
  };

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
          <div className="flex items-center space-x-4 relative">
            <span className="text-sm font-medium text-slate-500">Demo Mode Active</span>
            <button
              type="button"
              onClick={() => setProfileOpen(open => !open)}
              aria-label="Open profile menu"
              aria-expanded={profileOpen}
              className="h-8 w-8 bg-slate-200 rounded-full flex items-center justify-center text-slate-600 font-bold hover:bg-slate-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              {initials}
            </button>

            {profileOpen && (
              <div className="absolute right-0 top-11 z-10 w-56 bg-white border border-slate-200 rounded-lg shadow-lg p-4">
                <p className="text-sm font-semibold text-slate-800">{displayName}</p>
                <p className="text-xs text-slate-500 mt-1">{user?.email || 'Public Health Intelligence'}</p>
                <button
                  type="button"
                  onClick={() => { setSignupOpen(true); setProfileOpen(false); }}
                  className="w-full mt-3 px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 rounded-md"
                >
                  {user ? 'Create another account' : 'Sign up'}
                </button>
                <button
                  type="button"
                  onClick={() => setProfileOpen(false)}
                  className="w-full mt-3 px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 rounded-md"
                >
                  Close profile
                </button>
              </div>
            )}
          </div>
        </header>

        {signupOpen && (
          <div className="fixed inset-0 z-20 flex items-center justify-center bg-slate-900/40 p-4">
            <form onSubmit={handleSignup} className="w-full max-w-md bg-white rounded-xl shadow-xl p-6">
              <div className="flex items-center justify-between mb-5">
                <div>
                  <h2 className="text-lg font-semibold text-slate-800">Create your account</h2>
                  <p className="text-xs text-slate-500 mt-1">Set up a local demo profile.</p>
                </div>
                <button type="button" onClick={() => setSignupOpen(false)} className="text-slate-400 hover:text-slate-700" aria-label="Close sign up form">
                  X
                </button>
              </div>

              <div className="space-y-3">
                <input required value={signupForm.name} onChange={event => setSignupForm({ ...signupForm, name: event.target.value })} placeholder="Full name" className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm" />
                <input required type="email" value={signupForm.email} onChange={event => setSignupForm({ ...signupForm, email: event.target.value })} placeholder="Email address" className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm" />
                <select value={signupForm.role} onChange={event => setSignupForm({ ...signupForm, role: event.target.value })} className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm">
                  <option>Health Officer</option>
                  <option>ASHA Worker</option>
                  <option>Administrator</option>
                </select>
                <input required type="password" minLength="6" value={signupForm.password} onChange={event => setSignupForm({ ...signupForm, password: event.target.value })} placeholder="Password (6+ characters)" className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm" />
              </div>

              {signupError && <p className="mt-3 text-sm text-red-600">{signupError}</p>}
              <button type="submit" className="w-full mt-5 bg-primary-600 text-white py-2 rounded-md text-sm font-medium hover:bg-primary-700">
                Create account
              </button>
            </form>
          </div>
        )}
        
        <div className="flex-1 overflow-auto p-8">
          {children}
        </div>
      </main>
    </div>
  );
}