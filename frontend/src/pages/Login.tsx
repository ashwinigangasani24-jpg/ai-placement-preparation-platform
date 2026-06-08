import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

export default function Login() {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        const response = await api.post('/auth/login', {
          email,
          password
        });
        localStorage.setItem('token', response.data.access_token);
        navigate('/');
      } else {
        await api.post('/auth/register', {
          name,
          email,
          password
        });
        // Auto login after register
        const loginResponse = await api.post('/auth/login', {
          email,
          password
        });
        localStorage.setItem('token', loginResponse.data.access_token);
        navigate('/');
      }
    } catch (err: any) {
      console.error(err);
      let errDetail = err.response?.data?.detail;
      if (Array.isArray(errDetail)) {
        errDetail = errDetail.map((e: any) => `${e.loc?.join('.') || 'Field'}: ${e.msg}`).join(', ');
      } else if (typeof errDetail === 'object' && errDetail !== null) {
        errDetail = JSON.stringify(errDetail);
      }
      setError(errDetail || "Authentication failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background bg-gradient-radial from-surface/50 to-background p-6">
      <div className="glass-panel p-8 max-w-md w-full animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-primary to-accent flex items-center justify-center text-white font-bold text-3xl shadow-lg shadow-primary/30 mx-auto mb-4">
            AI
          </div>
          <h2 className="text-3xl font-bold">{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
          <p className="text-muted mt-2">
            {isLogin ? 'Sign in to access your dashboard' : 'Join to start your placement journey'}
          </p>
        </div>

        {error && (
          <div className="bg-red-500/20 border border-red-500/50 text-red-200 p-4 rounded-xl mb-6 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <div className="space-y-2">
              <label className="text-sm font-medium text-white/80">Full Name</label>
              <input 
                type="text" 
                required
                className="input-field w-full bg-[#1a1f2e]" 
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="John Doe"
              />
            </div>
          )}
          
          <div className="space-y-2">
            <label className="text-sm font-medium text-white/80">Email Address</label>
            <input 
              type="email" 
              required
              className="input-field w-full bg-[#1a1f2e]" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-white/80">Password</label>
            <input 
              type="password" 
              required
              className="input-field w-full bg-[#1a1f2e]" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="btn-primary w-full py-3 mt-4 disabled:opacity-50"
          >
            {loading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Sign Up')}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-muted">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button 
            type="button"
            onClick={() => setIsLogin(!isLogin)}
            className="text-primary hover:underline font-medium"
          >
            {isLogin ? 'Sign Up' : 'Sign In'}
          </button>
        </div>
      </div>
    </div>
  );
}
