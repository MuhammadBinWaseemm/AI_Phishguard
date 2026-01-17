import { AlertTriangle, CheckCircle, Zap } from 'lucide-react';

interface ResultCardProps {
  result: {
    prediction: string;
    confidence: number;
    reconstruction_error: number;
    is_phishing: boolean;
    risk_level: string;
  };
}

const ResultCard = ({ result }: ResultCardProps) => {
  const isPhishing = result.is_phishing;
  const confidence = result.confidence;

  const riskColors = {
    CRITICAL: 'from-red-600 to-red-700',
    HIGH: 'from-orange-600 to-red-600',
    MEDIUM: 'from-yellow-600 to-orange-600',
    LOW: 'from-green-600 to-emerald-600',
    SAFE: 'from-green-500 to-emerald-500',
    UNCERTAIN: 'from-gray-600 to-slate-600',
  };

  const riskBgColors = {
    CRITICAL: 'bg-red-500/10 border-red-500/50',
    HIGH: 'bg-orange-500/10 border-orange-500/50',
    MEDIUM: 'bg-yellow-500/10 border-yellow-500/50',
    LOW: 'bg-green-500/10 border-green-500/50',
    SAFE: 'bg-green-500/10 border-green-500/50',
    UNCERTAIN: 'bg-gray-500/10 border-gray-500/50',
  };

  const riskLevelColor = riskColors[result.risk_level as keyof typeof riskColors] || riskColors.UNCERTAIN;
  const riskBgColor = riskBgColors[result.risk_level as keyof typeof riskBgColors] || riskBgColors.UNCERTAIN;

  return (
    <div className="space-y-6">
      <div className={`relative overflow-hidden rounded-2xl border p-8 backdrop-blur-sm ${riskBgColor}`}>
        <div className={`absolute inset-0 bg-gradient-to-r ${riskLevelColor} opacity-5`}></div>

        <div className="relative flex flex-col items-center justify-center text-center">
          <div className="mb-6">
            {isPhishing ? (
              <div className="inline-block p-4 rounded-full bg-red-500/20 border border-red-400/50 animate-pulse">
                <AlertTriangle className="w-16 h-16 text-red-400" />
              </div>
            ) : (
              <div className="inline-block p-4 rounded-full bg-green-500/20 border border-green-400/50">
                <CheckCircle className="w-16 h-16 text-green-400" />
              </div>
            )}
          </div>

          <h1 className="text-5xl font-bold mb-4">
            {isPhishing ? (
              <span className="text-red-400">PHISHING DETECTED</span>
            ) : (
              <span className="text-green-400">EMAIL SAFE</span>
            )}
          </h1>

          <p className={`text-2xl font-semibold mb-2 ${
            isPhishing ? 'text-red-300' : 'text-green-300'
          }`}>
            {result.prediction.charAt(0).toUpperCase() + result.prediction.slice(1)} Email
          </p>

          <p className="text-gray-300 mb-6">
            Risk Level: <span className="font-bold text-lg">{result.risk_level}</span>
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-6 rounded-xl border border-blue-400/30 bg-blue-500/5 backdrop-blur-sm">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-5 h-5 text-blue-400" />
            <h3 className="text-sm font-semibold text-blue-300">Confidence Score</h3>
          </div>
          <div className="mt-4">
            <p className="text-4xl font-bold text-cyan-400">{(confidence * 100).toFixed(1)}%</p>
            <div className="mt-3 w-full bg-gray-700 rounded-full h-2 overflow-hidden">
              <div
                className={`h-full transition-all duration-300 rounded-full ${
                  isPhishing
                    ? 'bg-gradient-to-r from-red-500 to-orange-500'
                    : 'bg-gradient-to-r from-green-500 to-emerald-500'
                }`}
                style={{ width: `${confidence * 100}%` }}
              ></div>
            </div>
            <p className="text-xs text-gray-400 mt-2">
              {confidence > 0.9
                ? 'Very High Confidence'
                : confidence > 0.75
                ? 'High Confidence'
                : confidence > 0.6
                ? 'Moderate Confidence'
                : 'Low Confidence'}
            </p>
          </div>
        </div>

        <div className="p-6 rounded-xl border border-cyan-400/30 bg-cyan-500/5 backdrop-blur-sm">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-5 h-5 text-cyan-400" />
            <h3 className="text-sm font-semibold text-cyan-300">Anomaly Score</h3>
          </div>
          <div className="mt-4">
            <p className="text-4xl font-bold text-blue-400">{result.reconstruction_error.toFixed(4)}</p>
            <p className="text-xs text-gray-400 mt-2">
              Autoencoder reconstruction error. Higher = more anomalous.
            </p>
            <div className="mt-3 space-y-1 text-xs text-gray-400">
              <p>• Normal: 0.0-0.05</p>
              <p>• Borderline: 0.05-0.15</p>
              <p>• Suspicious: 0.15+</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4 md:grid-cols-6">
        <MetricBox label="Subject" value="Analyzed" icon="📧" />
        <MetricBox label="Body" value="Scanned" icon="📝" />
        <MetricBox label="Sender" value="Verified" icon="👤" />
        <MetricBox label="URLs" value="Checked" icon="🔗" />
        <MetricBox label="Keywords" value="Detected" icon="🔍" />
        <MetricBox label="AI Model" value="V1.0" icon="🤖" />
      </div>
    </div>
  );
};

const MetricBox = ({ label, value, icon }: { label: string; value: string; icon: string }) => (
  <div className="p-4 rounded-lg border border-gray-600/30 bg-gray-800/20 text-center hover:border-cyan-400/50 transition-colors duration-300">
    <div className="text-2xl mb-2">{icon}</div>
    <p className="text-xs text-gray-400 mb-1">{label}</p>
    <p className="text-sm font-semibold text-cyan-300">{value}</p>
  </div>
);

export default ResultCard;
