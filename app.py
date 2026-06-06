"""
Cyber4Africa MVP - AI Fraud Detection System
Flask backend for fraud detection dashboard.
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime
import os

app = Flask(__name__)

# Load model
model = joblib.load('model/fraud_model.pkl')
scaler = joblib.load('model/scaler.pkl')
features = joblib.load('model/features.pkl')

FEATURE_LABELS = {
    'amount': 'Transaction Amount (₦)',
    'hour': 'Hour of Day (0-23)',
    'day_of_week': 'Day of Week (0=Mon, 6=Sun)',
    'num_transactions_today': 'Transactions Today',
    'avg_transaction_amount': 'Avg. Transaction Amount (₦)',
    'account_age_days': 'Account Age (Days)',
    'failed_attempts': 'Failed Login Attempts',
    'is_international': 'International Transaction (0/1)',
    'device_change': 'New Device Used (0/1)',
    'location_change': 'Location Change (0/1)'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_transaction():
    try:
        data = request.get_json()
        values = [float(data.get(f, 0)) for f in features]
        df = pd.DataFrame([values], columns=features)
        scaled = scaler.transform(df)
        prediction = model.predict(scaled)[0]
        probability = model.predict_proba(scaled)[0]
        fraud_score = round(float(probability[1]) * 100, 1)

        # Risk level
        if fraud_score >= 70:
            risk = 'HIGH'
            color = '#ef4444'
        elif fraud_score >= 40:
            risk = 'MEDIUM'
            color = '#f59e0b'
        else:
            risk = 'LOW'
            color = '#10b981'

        # Feature importances
        importances = model.feature_importances_
        top_factors = sorted(
            zip(features, importances, values),
            key=lambda x: x[1], reverse=True
        )[:3]

        return jsonify({
            'prediction': int(prediction),
            'fraud_score': fraud_score,
            'risk_level': risk,
            'risk_color': color,
            'is_fraud': bool(prediction == 1),
            'top_factors': [
                {'feature': FEATURE_LABELS.get(f, f), 'importance': round(i*100, 1), 'value': v}
                for f, i, v in top_factors
            ],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/batch', methods=['POST'])
def batch_analyze():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No file uploaded'}), 400

        df = pd.read_csv(file)

        # Check for required features, fill missing with 0
        for f in features:
            if f not in df.columns:
                df[f] = 0

        X = df[features].fillna(0)
        scaled = scaler.transform(X)
        predictions = model.predict(scaled)
        probabilities = model.predict_proba(scaled)[:, 1]

        df['fraud_score'] = (probabilities * 100).round(1)
        df['prediction'] = predictions
        df['risk_level'] = df['fraud_score'].apply(
            lambda x: 'HIGH' if x >= 70 else ('MEDIUM' if x >= 40 else 'LOW')
        )

        results = df[['amount', 'fraud_score', 'risk_level', 'prediction']].to_dict(orient='records')

        return jsonify({
            'total': len(results),
            'fraud_count': int(predictions.sum()),
            'legitimate_count': int(len(predictions) - predictions.sum()),
            'high_risk': int((df['risk_level'] == 'HIGH').sum()),
            'medium_risk': int((df['risk_level'] == 'MEDIUM').sum()),
            'low_risk': int((df['risk_level'] == 'LOW').sum()),
            'results': results[:100]  # limit for display
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/demo', methods=['GET'])
def demo_data():
    """Return pre-analyzed demo transactions."""
    df = pd.read_csv('model/sample_transactions.csv')
    X = df[features].fillna(0)
    scaled = scaler.transform(X)
    predictions = model.predict(scaled)
    probabilities = model.predict_proba(scaled)[:, 1]

    df['fraud_score'] = (probabilities * 100).round(1)
    df['prediction'] = predictions
    df['risk_level'] = df['fraud_score'].apply(
        lambda x: 'HIGH' if x >= 70 else ('MEDIUM' if x >= 40 else 'LOW')
    )

    results = df[['amount', 'hour', 'num_transactions_today', 'account_age_days',
                  'is_international', 'fraud_score', 'risk_level', 'prediction']].head(20)

    return jsonify({
        'total': len(df),
        'fraud_count': int(predictions.sum()),
        'legitimate_count': int(len(predictions) - predictions.sum()),
        'results': results.to_dict(orient='records')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
