rom flask import Flask, request, jsonify
from joblib import load
import pandas as pd

app = Flask(name)
model = load('laptop_price_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        input_data = pd.DataFrame([{
            'brand': data['brand'],
            'model': data['model'],
            'ram': int(data['ram']),
            'storage': int(data['storage']),
            'screen_size': float(data['screen_size'])
        }])
        
        prediction = model.predict(input_data)
        return jsonify({
            'price': round(float(prediction[0])),
            'currency': 'USD',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

if name == 'main':
    app.run(host='0.0.0.0', port=5000)
