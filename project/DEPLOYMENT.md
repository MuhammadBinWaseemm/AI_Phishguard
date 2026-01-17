# Production Deployment Guide

Complete guide to deploy AI-PhishGuard to production.

## Table of Contents
1. [Backend Deployment (Railway)](#backend-deployment-railway)
2. [Frontend Deployment (Netlify)](#frontend-deployment-netlify)
3. [Custom Domain Setup](#custom-domain-setup)
4. [Environment Variables](#environment-variables)
5. [Monitoring & Logs](#monitoring--logs)

---

## Backend Deployment (Railway)

### Option 1: Railway.app (Recommended)

**Step 1: Create Railway Account**
- Go to https://railway.app
- Sign in with GitHub
- Click "New Project"

**Step 2: Connect Repository**
- Select "Deploy from GitHub"
- Authorize Railway to access your GitHub
- Select your `ai-phishguard` repository
- Select the branch (main/master)

**Step 3: Configure Backend**
- Railway should auto-detect Python
- Click "Add Service"
- Select "Python"

**Step 4: Set Environment Variables**
In Railway Dashboard → Variables:
```
PORT=8000
```

**Step 5: Configure Start Command**
In Railway Dashboard → Settings:
- **Start Command:** `python main.py`
- **Working Directory:** `backend`

**Step 6: Deploy**
- Click "Deploy"
- Watch logs for: `Uvicorn running on 0.0.0.0:8000`
- Copy deployment URL

**Step 7: Get Public URL**
In Railway Dashboard → Networking:
- Domain shows something like: `https://ai-phishguard-production-xyz.up.railway.app`

---

### Option 2: Render.com

**Step 1: Create Account**
- Go to https://render.com
- Sign up with GitHub

**Step 2: Create Web Service**
- Click "New +"
- Select "Web Service"
- Connect GitHub repository

**Step 3: Configure Service**
- **Name:** `ai-phishguard-backend`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python main.py`
- **Root Directory:** `backend` (if asked)

**Step 4: Deploy**
- Click "Create Web Service"
- Wait for deployment
- Copy public URL

---

## Frontend Deployment (Netlify)

### Step 1: Prepare Repository

Ensure your repo structure is:
```
project/
├── backend/
├── src/
├── package.json
├── vite.config.ts
└── (all frontend files)
```

### Step 2: Connect to Netlify

1. Go to https://netlify.com
2. Click "Add new site"
3. Select "Import an existing project"
4. Choose "GitHub"
5. Authorize Netlify to access your GitHub
6. Select your `ai-phishguard` repository

### Step 3: Configure Build Settings

In Netlify Dashboard:

- **Base directory:** (leave empty or root)
- **Build command:** `npm run build`
- **Publish directory:** `dist`

### Step 4: Add Environment Variables

In Netlify Dashboard → Site settings → Build & deploy → Environment:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://your-railway-backend-url` |

Replace `your-railway-backend-url` with your actual Railway/Render URL.

### Step 5: Deploy

- Click "Deploy site"
- Wait for build to complete
- Your site will be at: `https://your-site-name.netlify.app`

---

## Custom Domain Setup

### Add Custom Domain (Netlify)

1. Go to Site settings → Domain management
2. Click "Add domain"
3. Enter your domain (e.g., `phishguard.com`)
4. Update DNS records:

```
Type: CNAME
Name: www
Value: your-site-name.netlify.app
```

Or use Netlify's nameserver approach.

### SSL Certificate

Netlify automatically provides free SSL certificates. Your site will be:
- `https://your-domain.com`
- `https://www.your-domain.com`

---

## Environment Variables

### Frontend (.env.production)

```bash
VITE_API_URL=https://your-backend-production-url.com
```

### Backend (Railway/Render Variables)

```bash
PORT=8000
```

---

## Database Setup (Optional)

If you want to store prediction history:

### Create Supabase Project

1. Go to https://supabase.com
2. Create new project
3. Create table:

```sql
CREATE TABLE email_predictions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subject text,
  sender text,
  receiver text,
  prediction text,
  confidence float,
  risk_level text,
  created_at timestamp DEFAULT now()
);
```

### Update Backend Code

Add to `backend/main.py`:

```python
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.post("/predict")
async def predict(email: EmailInput):
    # ... existing code ...

    # Save to database
    supabase.table("email_predictions").insert({
        "subject": email.subject,
        "sender": email.sender,
        "receiver": email.receiver,
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "risk_level": result["risk_level"]
    }).execute()

    return result
```

---

## Monitoring & Logs

### Railway Logs
- Dashboard → Logs tab
- Filter by date/service
- Real-time log streaming

### Netlify Logs
- Site settings → Deploys
- Click deployment → Deploy log
- Shows build and runtime logs

### Performance Monitoring

**Check API Response Time:**
```bash
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
```

**Monitor Backend:**
- CPU usage in Railway dashboard
- Memory usage
- Request count

---

## Troubleshooting

### Backend won't start
```
Error: Models not found
```
Solution: Ensure `backend/models/` folder with model files is committed to git.

### CORS errors in frontend
```
Access to XMLHttpRequest blocked by CORS policy
```
Solution: Check `VITE_API_URL` environment variable matches backend URL exactly.

### Frontend doesn't load
```
Failed to fetch chunk
```
Solution: Clear browser cache, restart Netlify build.

### API timeout errors
```
Backend request timeout
```
Solution: Increase timeout in Railway/Render settings.

---

## Performance Optimization

### Frontend (Vite Build)
- Current size: ~622 kB (167 kB gzipped)
- Three.js included for 3D effects
- Minified and optimized

### Backend (FastAPI)
- Uvicorn ASGI server
- Sub-100ms inference time
- Connection pooling ready

### Recommendations
1. Enable CDN caching on Netlify
2. Set up Database connection pooling
3. Add Redis for model caching
4. Implement request rate limiting

---

## GitHub Actions CI/CD

Auto-deploy on push to main:

1. Go to GitHub → Settings → Secrets
2. Add secrets:
   - `RAILWAY_TOKEN` (from Railway)
   - `NETLIFY_TOKEN` (from Netlify)

3. Workflow file exists at `.github/workflows/test.yml`
4. On every push:
   - Runs tests
   - Builds frontend
   - Deploys to Netlify
   - Deploys to Railway

---

## Cost Estimation

### Monthly Costs (Estimate)

| Service | Free Tier | Paid |
|---------|-----------|------|
| Railway | 5 GB RAM free | $5-20 |
| Netlify | Unlimited builds | Free* |
| Supabase | 500 MB storage | $25+ |
| Total | **Free** | $30-45 |

*Netlify is free for static sites. Premium for advanced features.

---

## Rollback

If deployment fails:

**Railway:**
1. Dashboard → Deployments
2. Select previous version
3. Click "Redeploy"

**Netlify:**
1. Deploys → Select previous deployment
2. Click "Publish deploy"

---

## Production Checklist

- [ ] Backend deployed to Railway/Render
- [ ] Frontend deployed to Netlify
- [ ] Environment variables set correctly
- [ ] HTTPS/SSL working
- [ ] API endpoint responding
- [ ] Frontend loading without errors
- [ ] Email analysis working end-to-end
- [ ] Models are up-to-date
- [ ] Logs accessible
- [ ] Custom domain configured (optional)

---

## Support Resources

- Railway Docs: https://docs.railway.app
- Netlify Docs: https://docs.netlify.com
- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev

---

**Status:** ✅ Production Ready | **Last Updated:** 2024
