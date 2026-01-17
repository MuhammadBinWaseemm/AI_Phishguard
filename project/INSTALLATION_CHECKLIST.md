# Installation Checklist

Complete step-by-step checklist to get AI-PhishGuard running.

## Prerequisites ✓

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] npm installed
- [ ] Git installed
- [ ] 2GB free disk space

**Verify:**
```bash
python --version    # Should be 3.8+
node --version      # Should be 16+
npm --version       # Should be 8+
```

---

## Step 1: Clone Repository

- [ ] Clone the repository
- [ ] Navigate to project directory

```bash
git clone https://github.com/yourusername/ai-phishguard.git
cd ai-phishguard
```

---

## Step 2: Install Dependencies

### Frontend Dependencies

- [ ] Run npm install

```bash
npm install
```

**Expected:** ~248 packages installed, no errors

### Backend Dependencies

- [ ] Navigate to backend directory
- [ ] Run pip install

```bash
cd backend
pip install -r requirements.txt
cd ..
```

**Expected:** All packages installed successfully

**Verify:**
```bash
cd backend
python -c "import fastapi, pandas, numpy, sklearn; print('✓ All imports OK')"
cd ..
```

---

## Step 3: Prepare Dataset

Choose one option:

### Option A: Use Sample Dataset (Quick Test)

- [ ] Run sample dataset generator

```bash
cd backend
python sample_dataset.py
mv sample_combined.csv Combined.csv
cd ..
```

**Expected:** 100 sample emails created

### Option B: Use Your Own Dataset

- [ ] Prepare `Combined.csv` with columns: subject, body, sender, receiver, label
- [ ] Place file in `backend/` directory

**CSV Format:**
```
subject,body,sender,receiver,label
"Email Subject","Email body here","sender@email.com","receiver@email.com",0
```

---

## Step 4: Train Model

- [ ] Navigate to backend directory
- [ ] Run training script

```bash
cd backend
python train_model.py
```

**Expected Output:**
```
✓ Dataset loaded: 100 emails
✓ Features engineered successfully
✓ Models saved in: models/
✓ Training Complete!
```

**Verify Models Created:**
```bash
ls -lh models/
```

Should show:
- [ ] `scaler.pkl` (~1 MB)
- [ ] `autoencoder.pkl` (~2 MB)
- [ ] `random_forest.pkl` (~10 MB)
- [ ] `config.pkl` (~1 KB)

---

## Step 5: Start Backend Server

- [ ] Open Terminal 1
- [ ] Navigate to backend directory
- [ ] Start FastAPI server

```bash
cd backend
python main.py
```

**Expected Output:**
```
✓ All models loaded successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Verify Backend:**
```bash
# Open new terminal and test
curl http://localhost:8000/health
```

Should return:
```json
{"status": "healthy", "models_loaded": true}
```

---

## Step 6: Start Frontend Server

- [ ] Open Terminal 2
- [ ] Navigate to project root (not backend)
- [ ] Start Vite dev server

```bash
npm run dev
```

**Expected Output:**
```
VITE v5.0.0 ready in XXX ms

➜ Local:   http://localhost:5173/
➜ press h to show help
```

---

## Step 7: Verify Everything Works

### Check Frontend

- [ ] Open browser: `http://localhost:5173`
- [ ] Page loads without errors
- [ ] See "AI-PhishGuard" title
- [ ] 3D shield animation visible
- [ ] "Start Analysis" button visible

**Verify Console:** (Press F12)
- [ ] No red errors
- [ ] See "Analyzing email..." message when loading

### Check Backend Connection

- [ ] Click "Start Analysis" on frontend
- [ ] Fill in test form:
  - Sender: `test@example.com`
  - Receiver: `user@example.com`
  - Subject: `Test Subject`
  - Body: `Test email body`
- [ ] Click "Analyze Email"
- [ ] Wait for result
- [ ] See prediction result page

**Success Indicators:**
- [ ] Result page loads
- [ ] Shows "Email Safe" or "Phishing Detected"
- [ ] Shows confidence percentage
- [ ] Shows risk level

---

## Step 8: Test with Sample Emails

- [ ] Run test suite

```bash
python backend/test_emails.py
```

**Expected:** 5 test emails analyzed, results displayed

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue: "Models not found"

**Solution:**
```bash
cd backend
python train_model.py
```

### Issue: "Port 5173 already in use"

**Solution:**
```bash
npm run dev -- --port 3000
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
cd backend
python main.py --host 0.0.0.0 --port 8001
# Then update frontend .env.local:
# VITE_API_URL=http://localhost:8001
```

### Issue: CORS error in browser console

**Solution:**
1. Check `.env.local` has correct API URL
2. Ensure backend is running
3. Try clearing browser cache

### Issue: Frontend builds but nothing loads

**Solution:**
```bash
npm run build
npm run preview
```

---

## Environment Configuration

### Create `.env.local` (if needed)

```bash
# .env.local
VITE_API_URL=http://localhost:8000
```

For production, change to your actual backend URL.

---

## Verification Checklist

### Backend ✓

- [ ] `python main.py` starts without errors
- [ ] `/health` endpoint responds
- [ ] Models loaded successfully
- [ ] 4 model files in `backend/models/`

### Frontend ✓

- [ ] `npm run dev` starts without errors
- [ ] Page loads at `http://localhost:5173`
- [ ] No console errors
- [ ] Can navigate to analysis page
- [ ] Can submit email for analysis

### Integration ✓

- [ ] Frontend connects to backend
- [ ] Analysis returns results
- [ ] Results display correctly
- [ ] Multiple analyses work

---

## Next Steps

Once everything is working:

1. **Explore the code:**
   - Review `backend/main.py` for API logic
   - Check `src/App.tsx` for frontend structure
   - Examine `backend/train_model.py` for ML pipeline

2. **Customize:**
   - Update your dataset in `backend/Combined.csv`
   - Retrain model with `python train_model.py`
   - Customize UI in React components

3. **Deploy:**
   - Follow `DEPLOYMENT.md` for production setup
   - Deploy backend to Railway
   - Deploy frontend to Netlify

4. **Test:**
   - Use `backend/test_emails.py` for automated testing
   - Test with real emails
   - Monitor backend logs

---

## Getting Help

- **Setup Issues:** See `SETUP.md`
- **Deployment:** See `DEPLOYMENT.md`
- **Quick Start:** See `QUICKSTART.md`
- **General Info:** See `README.md`
- **Full Summary:** See `PROJECT_SUMMARY.md`

---

## Success Confirmation

✅ **You're ready when:**
- Backend server running on port 8000
- Frontend server running on port 5173
- Browser shows AI-PhishGuard home page
- Email analysis returns predictions
- No errors in browser console or terminal

---

**Estimated Setup Time:** 10-15 minutes

**Questions?** Check the documentation files included in the project.

Good luck! 🚀
