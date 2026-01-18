# PhishGuard: An Explainable AI Approach for Email Threat Detection

PhishGuard is a **hybrid, explainable AI-based email phishing detection system** that combines:
- Machine Learning (Random Forest)
- Anomaly Detection (Autoencoder)
- Rule-Based Analysis  

The system provides **accurate predictions with human-readable explanations** and is exposed through a **FastAPI backend**, with a separate **frontend (Node.js)** for interaction.

---

## 📁 Project Structure

AI_PhishGuard/
│
├── backend/
|
│ ├── main.py # FastAPI backend (prediction API)
|
│ ├── train_model.py # Model training pipeline
|
│ └── models/ # Generated ML models (created after training)
│
├── frontend/ # Node.js frontend (npm-based)
|
│ ├── node_modules/
|
│ ├── package.json
|
│ └── ...
│
├── .gitignore
|
├── README.md
|
└── requirements.txt (optional but recommended)


---

## ⚙️ Prerequisites

Make sure you have the following installed:

- **Python 3.9+**
- **pip**
- **Node.js (v16 or later)**
- **npm**
- **Git**

---

## 🚀 How to Run the Project (Step-by-Step)

### 1️⃣ Clone the Repository

git clone https://github.com/MuhammadBinWaseemm/AI_Phishguard.git
cd AI_Phishguard
### 2️⃣ Create and Activate Python Virtual Environment (venv)
On Windows (PowerShell)
python -m venv venv
venv\Scripts\activate
On Linux / macOS
python3 -m venv venv
source venv/bin/activate
### 3️⃣ Install Required Python Libraries
Install the required dependencies manually (or via requirements.txt if provided):

pip install fastapi uvicorn numpy pandas scikit-learn imbalanced-learn
📌 If you see any underlined import errors in the code (e.g., sklearn, numpy, pandas), install them using:

pip install <library-name>
Example:

pip install scikit-learn

### 4️⃣ Train the Machine Learning Models (IMPORTANT)
Before running the API, you must train the models first.

cd backend
python train_model.py
This will:

Train the Autoencoder and Random Forest

Create the models/ directory

Save trained .pkl files automatically

✅ Wait until you see “Training Complete!”

### 5️⃣ Run the FastAPI Backend
python main.py
OR (recommended):

uvicorn main:app --reload
Backend will start at:

http://127.0.0.1:8000
API Docs (Swagger UI):

http://127.0.0.1:8000/docs

### 6️⃣ Run the Frontend (Node.js)
Open a new terminal, navigate to the frontend folder:

cd frontend
npm install
npm run dev
Frontend will start at:

http://localhost:3000
(or the port shown in terminal)

🧪 Testing the System
Use the Swagger UI (/docs) to test email inputs

Or use the frontend UI

The system returns:

Prediction (Phishing / Legitimate)

Confidence score

Risk level

Explanation (Explainable AI output)

🔐 Detection Pipeline Overview
Feature Extraction from email content

Rule-Based Detection (for obvious cases)

Autoencoder (anomaly detection)

Random Forest classification

Hybrid decision + explanation

🧠 Notes
The models/ folder is generated automatically after training

Do not push venv/ or trained models to GitHub

Retrain models if dataset or features are modified

📌 Use Cases
Cybersecurity academic projects (FYP)

Email security gateways

Explainable AI demonstrations

Research & experimentation

📜 License
This project is for educational and research purposes.

✨ Author

Muhammmad Abdullah Khan Mahsud

Muhammad Bin Waseem

Muhammad Zaeem Nawaz

Muhammad Shaheer


