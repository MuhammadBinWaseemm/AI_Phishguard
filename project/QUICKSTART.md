# Quick Start Guide - 5 Minutes

Get AI-PhishGuard running in 5 minutes!

## Step 1: Install Dependencies (2 min)

```bash
# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

## Step 2: Create Sample Dataset (1 min)

```bash
cd backend
python sample_dataset.py
mv sample_combined.csv Combined.csv
```

This creates 100 sample emails automatically.

## Step 3: Train Model (2 min)

```bash
python train_model.py
```

Wait for it to finish. You'll see:
```
✓ Training Complete!
✓ Models saved in: models/
```

## Step 4: Start Backend

Open **Terminal 1**:
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✓ All models loaded successfully
```

## Step 5: Start Frontend

Open **Terminal 2**:
```bash
npm run dev
```

You should see:
```
VITE v5.0.0 ready in 234 ms

➜ Local:   http://localhost:5173/
```

## Step 6: Test It!

1. Open browser: `http://localhost:5173`
2. Click "Start Analysis"
3. Fill in test email:
   - **Sender:** `noreply@bank.com`
   - **Receiver:** `user@gmail.com`
   - **Subject:** `Urgent: Verify Your Account`
   - **Body:** `Click here to verify your account immediately: https://fake-site.com`
4. Click "Analyze Email"
5. See the prediction!

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
cd backend
pip install -r requirements.txt
```

### "Models not found"
```bash
cd backend
python train_model.py
```

### "Port 5173 in use"
```bash
npm run dev -- --port 3000
```

### "Port 8000 in use"
```bash
cd backend
python main.py --port 8001
```

---

## What's Next?

- 📖 Read [SETUP.md](./SETUP.md) for detailed configuration
- 🚀 Deploy to production (see SETUP.md)
- 🧪 Run test suite: `python backend/test_emails.py`
- 💾 Use your own dataset instead of sample data

---

**That's it!** You now have a fully working AI-PhishGuard system! 🎉
