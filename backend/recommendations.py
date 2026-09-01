from flask import Blueprint, request, jsonify
from config import PRODUCTS_DB_PATH
import json
from ..models.ml_model import ml

bp = Blueprint('recommendations', __name__, url_prefix='/api')

def load_products():
    with open(PRODUCTS_DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

@bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        
        temperature = float(data.get('temperature', 15))
        budget = float(data.get('budget', 15))
        month = int(data.get('month', 1))
        day = int(data.get('day', 0))
        
        prediction = ml.predict(temperature, budget, month, day)
        
        products = load_products()
        recommended = [p for p in products['products'] 
                      if p['category'] == prediction['category']]
        
        recommended = recommended[:6]
        
        return jsonify({
            'statut': 'succes',
            'prediction': prediction,
            'recommended_products': recommended,
            'message': f"Nous vous recommandons les {prediction['category']}"
        }), 200
    
    except Exception as e:
        return jsonify({
            'erreur': str(e),
            'statut': 'erreur'
        }), 500