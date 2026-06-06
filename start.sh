#!/bin/bash
# FraudShield AI - Startup Script
echo "🚀 Starting FraudShield AI MVP..."

# Train model if not already trained
if [ ! -f "model/fraud_model.pkl" ]; then
  echo "🤖 Training fraud detection model..."
  python train_model.py
fi

# Start the app
echo "🌐 Starting web server on port 5000..."
python app.py
