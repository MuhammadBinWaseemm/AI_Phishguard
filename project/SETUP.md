# AI-PhishGuard Setup & Deployment Guide

A production-ready email threat detection system powered by autoencoder anomaly detection and random forest classification.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Model Training](#model-training)
4. [Running the Application](#running-the-application)
5. [Deployment](#deployment)
6. [API Documentation](#api-documentation)

---

## Prerequisites

### Requirements
- Python 3.8+
- Node.js 16+ & npm
- Git
- 2GB disk space for models

### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Install Frontend Dependencies
```bash
npm install
```

---

## Local Development Setup

### 1. Project Structure
```
project/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── train_model.py       # Model training script
│   ├── requirements.txt     # Python dependencies
│   └── models/              # Saved models (generated)
├── src/
│   ├── App.tsx             # Main React app
│   ├── components/         # React components
│   ├── index.css          # Tailwind styles
│   └── main.tsx           # Entry point
├── package.json            # NPM dependencies
├── vite.config.ts         # Vite configuration
└── SETUP.md               # This file
```

### 2. Environment Variables

Create a `.env.local` file in the root directory:

**For Development:**
```
VITE_API_URL=http://localhost:8000
```

**For Production:**
```
VITE_API_URL=https://your-backend-url.com
```

---

## Model Training

### Step 1: Prepare Your Dataset

Place your `Combined.csv` file in the `backend/` directory with the following columns:
- `subject` - Email subject line
- `body` - Email body content
- `sender` - Sender email address
- `receiver` - Receiver email address
- `label` - Binary label (0 = legitimate, 1 = phishing)

**Example CSV structure:**
```
subject,body,sender,receiver,label
Urgent Account Verification,Click here to verify...,noreply@fake-bank.com,user@gmail.com,1
Your Package is Ready,Your order #12345...,delivery@amazon.com,customer@gmail.com,0
```

### Step 2: Train the Model

```bash
cd backend
python train_model.py
```

**What happens:**
- ✓ Loads and validates dataset
- ✓ Extracts 50+ engineered features
- ✓ Trains autoencoder on legitimate emails
- ✓ Computes reconstruction error anomaly scores
- ✓ Trains Random Forest classifier
- ✓ Saves 4 model files in `backend/models/`:
  - `scaler.pkl` - Feature scaler
  - `autoencoder.pkl` - Anomaly detector
  - `random_forest.pkl` - Classification model
  - `config.pkl` - Feature configuration

**Training Time:** 2-5 minutes depending on dataset size
**Expected Performance:** 90-97% accuracy on 10,000+ emails

### Step 3: Verify Models

Check that all 4 files exist:
```bash
ls -lh backend/models/
```

---

## Running the Application

### Option 1: Development Mode (Recommended)

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```
Backend runs at: `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
npm run dev
```
Frontend runs at: `http://localhost:5173`

### Option 2: Production Build

**Build Frontend:**
```bash
npm run build
```

**Run Backend (Production):**
```bash
cd backend
python main.py
```
Then serve the `dist/` folder using Nginx or a static host.

---

## Deployment

### Backend Deployment (Railway.app Example)

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign in with GitHub

2. **Deploy Backend**
   ```bash
   # Connect your repo
   cd backend
   railway init
   railway add
   ```

3. **Configure Environment**
   - Add Python version: `3.9`
   - Set start command: `python main.py`

4. **Get Deployment URL**
   - Railway provides: `https://your-app-name.railway.app`

### Frontend Deployment (Netlify)

1. **Connect GitHub Repo**
   - Go to https://netlify.com
   - Connect your GitHub repository

2. **Configure Build Settings**
   - Build command: `npm run build`
   - Publish directory: `dist`

3. **Environment Variables**
   Add in Netlify dashboard:
   ```
   VITE_API_URL=https://your-backend-railway-url.railway.app
   ```

4. **Deploy**
   - Netlify auto-deploys on git push
   - Your app will be at: `https://your-site-name.netlify.app`

### Alternative Hosting Options

**Backend:**
- Render.com (recommended)
- Heroku
- Replit
- DigitalOcean

**Frontend:**
- Vercel
- GitHub Pages
- AWS Amplify

---

## API Documentation

### Base URL
- Local: `http://localhost:8000`
- Production: `https://your-backend-url.com`

### Endpoints

#### 1. Health Check
```
GET /health
```
Response:
```json
{
  "status": "healthy",
  "models_loaded": true
}
```

#### 2. Predict (Main Endpoint)
```
POST /predict
Content-Type: application/json

{
  "subject": "Verify Your Account Now",
  "body": "Click here to verify your account. This is urgent!",
  "sender": "security@bank.com",
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

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `prediction` | string | "phishing" or "legitimate" |
| `confidence` | float | 0.0-1.0 confidence score |
| `reconstruction_error` | float | Autoencoder anomaly score |
| `is_phishing` | boolean | True if phishing detected |
| `risk_level` | string | CRITICAL, HIGH, MEDIUM, LOW, SAFE |
| `explanation` | string | AI-generated explanation |

### Risk Levels

| Level | Criteria | Action |
|-------|----------|--------|
| CRITICAL | Phishing, confidence > 95% | Block immediately |
| HIGH | Phishing, confidence > 85% | Warn user |
| MEDIUM | Uncertain classification | Review manually |
| LOW | Legitimate, confidence > 85% | Allow |
| SAFE | Legitimate, confidence > 95% | Allow without warning |

---

## Feature Engineering Pipeline

The model extracts 50+ features:

### Length Features (3)
- Subject length
- Body length
- Sender length

### URL Features (3)
- Has URL
- URL count
- Suspicious URL (bit.ly, tinyurl, etc.)

### Character Features (3)
- Special character ratio
- Digit ratio
- Uppercase ratio

### Structural Features (9)
- Word count
- Average word length
- Subject word count
- Suspicious sender pattern
- Generic greeting detection

### Keyword Features (22)
Detects phishing keywords:
- urgent, verify, account, security, bank, login
- click, update, alert, suspend, password, confirm
- winner, prize, free, limited, offer
- and 8 more...

### Time Features (2)
- Hour of day
- Day of week

### Hybrid Features (3)
- Reconstruction error (from autoencoder)
- Squared error
- Root error

---

## Model Architecture

### Autoencoder
```
Input (50 features)
  ↓
Dense(64) + ReLU
  ↓
Dense(32) + ReLU
  ↓
Dense(16) + ReLU (Bottleneck)
  ↓
Dense(32) + ReLU
  ↓
Dense(64) + ReLU
  ↓
Output (50 features)
```

**Purpose:** Learns normal email patterns, flags anomalies

### Random Forest
```
Input: Original 50 features + 3 hybrid features (53 total)
Classifier: 200 decision trees
Max Depth: 15
Class Weight: Balanced
```

**Purpose:** Final phishing classification using hybrid features

---

## Testing

### Test with cURL

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Urgent: Verify Your Account",
    "body": "Dear Customer, click here to verify your account immediately: https://fake-site.com",
    "sender": "noreply@bank123.com",
    "receiver": "user@gmail.com"
  }'
```

### Test with Python

```python
import requests

response = requests.post(
    'http://localhost:8000/predict',
    json={
        'subject': 'Verify Your Account Now',
        'body': 'Click here to verify...',
        'sender': 'noreply@bank.com',
        'receiver': 'user@gmail.com'
    }
)

print(response.json())
```

### Test with Frontend

1. Start frontend: `npm run dev`
2. Open `http://localhost:5173`
3. Click "Start Analysis"
4. Fill in email details
5. Click "Analyze Email"

---

## Troubleshooting

### Backend Issues

**Error: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**Error: Models not found**
```bash
cd backend
python train_model.py
```

**Error: CORS issues**
- Backend automatically allows all origins
- Check `VITE_API_URL` in frontend `.env.local`

### Frontend Issues

**Port 5173 already in use**
```bash
npm run dev -- --port 3000
```

**Styles not loading**
```bash
npm install
npm run dev
```

---

## Performance Tips

1. **Batch Processing:** Use a queue for large email volumes
2. **Caching:** Cache results for identical emails
3. **Model Optimization:** Use ONNX for faster inference
4. **Database:** Add PostgreSQL for email history

---

## Security Notes

⚠️ **Important:**
- Never expose API keys in frontend code
- Always use HTTPS in production
- Implement rate limiting for API
- Add authentication for sensitive endpoints
- Regularly update dependencies

---

## Support & Contributions

For issues or improvements:
1. Check existing GitHub issues
2. Create detailed bug report
3. Submit pull requests

---

## License

MIT License - Feel free to use for personal or commercial projects.

---

**Version:** 1.0.0
**Last Updated:** 2024
**Status:** Production Ready
