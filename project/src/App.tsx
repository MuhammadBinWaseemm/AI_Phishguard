import { useState } from 'react';
import { Shield, AlertTriangle, CheckCircle, Loader, Zap } from 'lucide-react';
import ThreeScene from './components/ThreeScene';
import AnalysisForm from './components/AnalysisForm';
import ResultCard from './components/ResultCard';
import './index.css';

interface PredictionResult {
  prediction: string;
  confidence: number;
  reconstruction_error: number;
  is_phishing: boolean;
  risk_level: string;
  explanation: string;
}

function App() {
  const [page, setPage] = useState<'home' | 'analyze' | 'result'>('home');
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (emailData: {
    subject: string;
    body: string;
    sender: string;
    receiver: string;
  }) => {
    setLoading(true);
    setError(null);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(emailData),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze email');
      }

      const data = await response.json();
      setResult(data);
      setPage('result');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setPage('home');
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white overflow-hidden">
      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }
        @keyframes pulse-glow {
          0%, 100% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.5), inset 0 0 20px rgba(59, 130, 246, 0.1); }
          50% { box-shadow: 0 0 40px rgba(59, 130, 246, 0.8), inset 0 0 40px rgba(59, 130, 246, 0.2); }
        }
        @keyframes scan {
          0%, 100% { box-shadow: inset 0 0 0 rgba(34, 197, 94, 0.5); }
          50% { box-shadow: inset 0 0 20px rgba(34, 197, 94, 0.8); }
        }
        @keyframes text-glow {
          0%, 100% { text-shadow: 0 0 10px rgba(59, 130, 246, 0.5); }
          50% { text-shadow: 0 0 20px rgba(59, 130, 246, 0.9), 0 0 30px rgba(59, 130, 246, 0.6); }
        }
        @keyframes particles {
          0% { transform: translate(0, 0) scale(1); opacity: 1; }
          100% { transform: translate(var(--tx), var(--ty)) scale(0); opacity: 0; }
        }
        .float-animation { animation: float 3s ease-in-out infinite; }
        .pulse-glow { animation: pulse-glow 2s ease-in-out infinite; }
        .scan-effect { animation: scan 2s ease-in-out infinite; }
        .text-glow { animation: text-glow 2s ease-in-out infinite; }
      `}</style>

      {page === 'home' && (
        <div className="relative min-h-screen flex flex-col">
          <ThreeScene />

          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-20 left-10 w-2 h-2 bg-blue-400 rounded-full opacity-50"></div>
            <div className="absolute top-40 right-20 w-3 h-3 bg-cyan-400 rounded-full opacity-30"></div>
            <div className="absolute bottom-40 left-1/4 w-2 h-2 bg-blue-300 rounded-full opacity-40"></div>
          </div>

          <div className="relative z-10 flex-1 flex flex-col items-center justify-center px-4">
            <div className="mb-12 text-center float-animation">
              <div className="inline-block p-4 mb-6 rounded-full bg-gradient-to-r from-blue-500/20 to-cyan-500/20 border border-blue-400/50 pulse-glow">
                <Shield className="w-16 h-16 text-blue-400" />
              </div>
            </div>

            <h1 className="text-6xl md:text-7xl font-bold mb-4 text-center text-glow">
              AI-PhishGuard
            </h1>

            <p className="text-2xl md:text-3xl text-center mb-8 text-cyan-300">
              Real-Time Email Threat Detection
            </p>

            <p className="max-w-2xl text-center text-gray-300 mb-12 text-lg">
              Advanced machine learning powered by autoencoder anomaly detection and random forest classification
            </p>

            <button
              onClick={() => setPage('analyze')}
              className="group relative px-8 py-4 text-lg font-semibold rounded-lg overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-cyan-500"></div>
              <span className="relative flex items-center justify-center gap-2">
                <Zap className="w-5 h-5" />
                Start Analysis
              </span>
            </button>

            <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl">
              {[
                { title: 'Advanced ML', desc: 'Autoencoder + Random Forest' },
                { title: 'Real-Time', desc: 'Instant threat detection' },
                { title: 'Secure', desc: 'Privacy-first analysis' }
              ].map((item, i) => (
                <div key={i} className="p-6 rounded-lg border border-blue-400/30 bg-blue-500/5 hover:border-cyan-400/50 hover:bg-cyan-500/10 transition-all duration-300">
                  <h3 className="text-cyan-300 font-semibold mb-2">{item.title}</h3>
                  <p className="text-gray-400">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {page === 'analyze' && (
        <div className="relative min-h-screen py-12 px-4">
          <div className="absolute top-0 left-0 w-full h-96 bg-gradient-to-b from-blue-500/5 to-transparent pointer-events-none"></div>

          <div className="relative z-10 max-w-4xl mx-auto">
            <button
              onClick={handleReset}
              className="mb-8 px-4 py-2 text-sm text-gray-400 hover:text-cyan-300 transition-colors"
            >
              ← Back Home
            </button>

            <div className="mb-8">
              <h1 className="text-4xl md:text-5xl font-bold mb-4 text-glow">Analyze Email</h1>
              <p className="text-gray-400">Enter email details for real-time threat detection</p>
            </div>

            <AnalysisForm
              onSubmit={handleAnalyze}
              loading={loading}
              error={error}
            />
          </div>
        </div>
      )}

      {page === 'result' && result && (
        <div className="relative min-h-screen py-12 px-4">
          <div className="absolute top-0 left-0 w-full h-full pointer-events-none overflow-hidden">
            {result.is_phishing ? (
              <div className="absolute inset-0 opacity-10 bg-red-500 animate-pulse"></div>
            ) : (
              <div className="absolute inset-0 opacity-10 bg-green-500 animate-pulse"></div>
            )}
          </div>

          <div className="relative z-10 max-w-2xl mx-auto">
            <button
              onClick={handleReset}
              className="mb-8 px-4 py-2 text-sm text-gray-400 hover:text-cyan-300 transition-colors"
            >
              ← Analyze Another Email
            </button>

            <ResultCard result={result} />

            <div className="mt-8 p-6 rounded-lg border border-gray-700/50 bg-slate-800/50 backdrop-blur-sm">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Zap className="w-5 h-5 text-cyan-400" />
                AI Analysis
              </h3>
              <p className="text-gray-300 leading-relaxed">{result.explanation}</p>
            </div>
          </div>
        </div>
      )}

      {loading && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="text-center">
            <div className="inline-block p-6 rounded-full bg-gradient-to-r from-blue-500/20 to-cyan-500/20 border border-blue-400/50 pulse-glow mb-6">
              <Loader className="w-12 h-12 text-blue-400 animate-spin" />
            </div>
            <p className="text-xl text-cyan-300">Analyzing email...</p>
            <p className="text-sm text-gray-400 mt-2">Running threat detection algorithms</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
