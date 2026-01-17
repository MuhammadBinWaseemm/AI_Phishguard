import { useState } from 'react';
import { Send, AlertCircle } from 'lucide-react';

interface AnalysisFormProps {
  onSubmit: (data: {
    subject: string;
    body: string;
    sender: string;
    receiver: string;
  }) => void;
  loading: boolean;
  error: string | null;
}

const AnalysisForm = ({ onSubmit, loading, error }: AnalysisFormProps) => {
  const [formData, setFormData] = useState({
    subject: '',
    body: '',
    sender: '',
    receiver: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.subject && formData.body && formData.sender && formData.receiver) {
      onSubmit(formData);
    }
  };

  const isValid = formData.subject && formData.body && formData.sender && formData.receiver;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/50 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
          <p className="text-red-200">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-semibold text-cyan-300 mb-2">
            Sender Email
          </label>
          <input
            type="email"
            name="sender"
            value={formData.sender}
            onChange={handleChange}
            placeholder="sender@example.com"
            className="w-full px-4 py-3 rounded-lg bg-slate-800/50 border border-blue-400/30 text-white placeholder-gray-500 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/20 transition-all duration-300"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-cyan-300 mb-2">
            Receiver Email
          </label>
          <input
            type="email"
            name="receiver"
            value={formData.receiver}
            onChange={handleChange}
            placeholder="receiver@example.com"
            className="w-full px-4 py-3 rounded-lg bg-slate-800/50 border border-blue-400/30 text-white placeholder-gray-500 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/20 transition-all duration-300"
            required
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-semibold text-cyan-300 mb-2">
          Email Subject
        </label>
        <input
          type="text"
          name="subject"
          value={formData.subject}
          onChange={handleChange}
          placeholder="Email subject line..."
          className="w-full px-4 py-3 rounded-lg bg-slate-800/50 border border-blue-400/30 text-white placeholder-gray-500 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/20 transition-all duration-300"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-semibold text-cyan-300 mb-2">
          Email Body
        </label>
        <textarea
          name="body"
          value={formData.body}
          onChange={handleChange}
          placeholder="Paste the email body content here..."
          rows={8}
          className="w-full px-4 py-3 rounded-lg bg-slate-800/50 border border-blue-400/30 text-white placeholder-gray-500 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/20 transition-all duration-300 resize-none"
          required
        />
      </div>

      <div className="flex gap-4 pt-4">
        <button
          type="submit"
          disabled={!isValid || loading}
          className={`flex-1 relative px-6 py-3 text-lg font-semibold rounded-lg overflow-hidden group transition-all duration-300 ${
            !isValid || loading ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105'
          }`}
        >
          <div className={`absolute inset-0 bg-gradient-to-r ${
            !isValid || loading ? 'from-gray-600 to-gray-600' : 'from-blue-600 to-cyan-600 opacity-0 group-hover:opacity-100'
          } transition-opacity duration-300`}></div>
          <div className={`absolute inset-0 bg-gradient-to-r ${
            !isValid || loading ? 'from-gray-500 to-gray-500' : 'from-blue-500 to-cyan-500'
          }`}></div>
          <span className="relative flex items-center justify-center gap-2">
            <Send className="w-5 h-5" />
            {loading ? 'Analyzing...' : 'Analyze Email'}
          </span>
        </button>
      </div>

      <p className="text-xs text-gray-400 text-center">
        Your email is analyzed locally for threat detection. No data is stored.
      </p>
    </form>
  );
};

export default AnalysisForm;
