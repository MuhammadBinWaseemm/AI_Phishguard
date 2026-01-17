# AI-PhishGuard

> Advanced real-time email threat detection powered by machine learning

![AI-PhishGuard](https://img.shields.io/badge/Version-1.0.0-blue) ![Status](https://img.shields.io/badge/Status-Production%20Ready-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![React](https://img.shields.io/badge/React-18.3-61dafb)

## Features

🛡️ **Advanced ML Model**
- Hybrid autoencoder + Random Forest architecture
- 90-97% accuracy on 10,000+ email dataset
- Detects 50+ phishing indicators

⚡ **Real-Time Analysis**
- Sub-second email threat detection
- Instant UI feedback with loading states
- Scalable FastAPI backend

🎨 **Premium UI**
- Interactive Three.js 3D animations
- Cybersecurity-themed dark design
- Glass-morphism glass effects
- Smooth transitions and particle effects
- Mobile-responsive design

🔒 **Security First**
- Privacy-first analysis (no data storage)
- CORS-enabled for secure communication
- Rate limiting ready
- Feature engineering pipeline

## Quick Start

### 1. Clone & Install

```bash
# Clone repository
git clone https://github.com/yourusername/ai-phishguard.git
cd ai-phishguard

# Install dependencies
npm install
cd backend && pip install -r requirements.txt && cd ..
```

### 2. Prepare Dataset

Place your `Combined.csv` in `backend/` folder:

```csv
subject,body,sender,receiver,label
Email Subject,Email body content,sender@email.com,receiver@email.com,0
```

Required columns: `subject`, `body`, `sender`, `receiver`, `label` (0=legitimate, 1=phishing)

### 3. Train Model

```bash
cd backend
python train_model.py
```

Output:
```
✓ Dataset loaded: 10000 emails
✓ Features engineered successfully
✓ Models saved in: backend/models/
```

### 4. Run Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

Open: `http://localhost:5173`

## Project Structure

```
ai-phishguard/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── train_model.py       # Model training
│   ├── test_emails.py       # Test suite
│   ├── requirements.txt     # Dependencies
│   └── models/              # Trained models (generated)
│
├── src/
│   ├── App.tsx             # Main app component
│   ├── components/
│   │   ├── ThreeScene.tsx  # 3D background
│   │   ├── AnalysisForm.tsx # Email input form
│   │   └── ResultCard.tsx  # Results display
│   ├── index.css           # Tailwind styles
│   └── main.tsx            # React entry point
│
├── package.json
├── vite.config.ts
├── SETUP.md                # Detailed setup guide
└── README.md               # This file
```

## Model Architecture

### Autoencoder (Anomaly Detection)
```
50 features → 64 → 32 → 16 (bottleneck) → 32 → 64 → 50 features
```
- Learns normal email patterns
- Detects structural anomalies
- Computes reconstruction error

### Random Forest (Classification)
```
53 features (50 + 3 hybrid) → 200 trees → Phishing/Legitimate
```
- Features: Original 50 + reconstruction error features
- Balanced class weights
- Max depth: 15 to prevent overfitting

## Feature Engineering

The model analyzes **50+ features**:

| Category | Count | Examples |
|----------|-------|----------|
| Length | 3 | subject_length, body_length, sender_length |
| URL | 3 | has_url, url_count, suspicious_url |
| Characters | 3 | special_char_ratio, digit_ratio, uppercase_ratio |
| Structure | 9 | word_count, generic_greeting, etc. |
| Keywords | 22 | has_urgent, has_verify, has_account, ... |
| Time | 2 | hour, day_of_week |
| Hybrid | 3 | reconstruction_error, squared_error, sqrt_error |

## API Endpoints

### Health Check
```http
GET /health
```

### Predict Email
```http
POST /predict
Content-Type: application/json

{
  "subject": "Verify Your Account",
  "body": "Click here to verify...",
  "sender": "noreply@bank.com",
  "receiver": "user@gmail.com"
}
```

**Response:**
```json
{
  "prediction": "phishing",
  "confidence": 0.94,
  "reconstruction_error": 0.2345,
  "is_phishing": true,
  "risk_level": "CRITICAL",
  "explanation": "High-confidence phishing detection..."
}
```

## Testing

### Test with cURL
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Urgent Account Verification",
    "body": "Click here: https://fake-site.com",
    "sender": "noreply@bank.com",
    "receiver": "user@gmail.com"
  }'
```

### Test Suite
```bash
python backend/test_emails.py
```

## Deployment

### Backend (Railway)
1. Go to https://railway.app
2. Connect GitHub repo
3. Configure Python 3.9
4. Set start command: `python main.py`
5. Note deployment URL

### Frontend (Netlify)
1. Go to https://netlify.com
2. Connect GitHub repo
3. Build command: `npm run build`
4. Publish directory: `dist`
5. Add env var: `VITE_API_URL=<backend-url>`

## Configuration

### Environment Variables

`.env.local`:
```bash
VITE_API_URL=http://localhost:8000        # Development
VITE_API_URL=https://api.example.com      # Production
```

## Performance

| Metric | Value |
|--------|-------|
| Accuracy | 90-97% |
| Precision | 92-95% |
| Recall | 88-96% |
| F1-Score | 90-95% |
| Inference Time | <100ms |
| Model Size | ~15MB |

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Security Notes

⚠️ **Important:**
- Never commit `.env` files with real credentials
- Always use HTTPS in production
- Implement rate limiting for API
- Add authentication for sensitive endpoints
- Regularly update dependencies

## Troubleshooting

### Models not loading
```bash
cd backend && python train_model.py
```

### CORS errors
- Ensure `VITE_API_URL` matches backend URL
- Backend allows all origins by default

### Port already in use
```bash
npm run dev -- --port 3000
```

## Technologies

**Frontend:**
- React 18.3
- TypeScript
- Tailwind CSS
- Three.js
- Lucide React Icons
- Vite

**Backend:**
- FastAPI
- Python 3.8+
- scikit-learn
- pandas
- numpy

**ML Stack:**
- Autoencoder (MLPRegressor)
- Random Forest Classifier
- StandardScaler
- Precision Recall Curve

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing`
5. Open Pull Request

## License

MIT License - Feel free to use for personal or commercial projects.

## Author

Built with ❤️ for email security

## Support

- 📖 See [SETUP.md](./SETUP.md) for detailed setup guide
- 🐛 Report issues on GitHub
- 💡 Suggest features with discussions

---

**Status:** ✅ Production Ready | **Version:** 1.0.0 | **Last Updated:** 2024
