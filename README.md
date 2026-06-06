# 🛡️ FraudShield AI — MVP

AI-powered fraud detection system for African financial institutions.
Built for the **Cyber4Africa Programme** by the AI Hub for Sustainable Development.

---

## 🚀 Quick Start (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train the model
python train_model.py

# 3. Run the app
python app.py

# 4. Open browser
# http://localhost:5000
```

---

## ☁️ Deploy to Render.com (Free - 5 mins)

1. Push this folder to a GitHub repository
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Set these settings:
   - **Build Command:** `pip install -r requirements.txt && python train_model.py`
   - **Start Command:** `gunicorn app:app`
5. Click **Deploy** — you'll get a live URL!

---

## ☁️ Deploy to Railway.app (Free alternative)

1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Add environment variable: `PORT=5000`
4. Done!

---

## 🔌 API Endpoints

### Single Transaction Analysis
```
POST /api/analyze
Content-Type: application/json

{
  "amount": 25000,
  "hour": 14,
  "day_of_week": 2,
  "num_transactions_today": 3,
  "avg_transaction_amount": 18000,
  "account_age_days": 365,
  "failed_attempts": 0,
  "is_international": 0,
  "device_change": 0,
  "location_change": 0
}
```

### Batch Analysis
```
POST /api/batch
Content-Type: multipart/form-data
file: transactions.csv
```

### Demo Data
```
GET /api/demo
```

---

## 🤖 Model Details

- **Algorithm:** Random Forest Classifier
- **Features:** 10 transaction features
- **Training Data:** 10,000 synthetic transactions (97% legitimate, 3% fraud)
- **Accuracy:** 99.8%
- **Fraud Recall:** 98%

---

## 📁 Project Structure

```
fraud-mvp/
├── app.py              # Flask web application
├── train_model.py      # Model training script
├── requirements.txt    # Python dependencies
├── start.sh           # Startup script
├── model/
│   ├── fraud_model.pkl     # Trained model
│   ├── scaler.pkl          # Data scaler
│   ├── features.pkl        # Feature list
│   └── sample_transactions.csv
└── templates/
    └── index.html      # Dashboard UI
```

---

## 🌍 Built for Africa

Designed for Nigerian and African financial institutions. Transaction amounts
displayed in Naira (₦). Adaptable for any African currency.

---

*Cyber4Africa Programme · AI Hub for Sustainable Development · 2026*
