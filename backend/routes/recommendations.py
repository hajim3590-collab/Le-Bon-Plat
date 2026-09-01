from flask import Blueprint, request, jsonify
import json
import sys
import os

# Importer depuis le répertoire parent (backend/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PRODUCTS_DB_PATH
from models.ml_model import ml

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

        print(f"📊 Recommandation reçue: temp={temperature}, budget={budget}, month={month}, day={day}")

        prediction = ml.predict(temperature, budget, month, day)
        print(f"🤖 Prédiction du modèle: {prediction}")

        products = load_products()
        print(f"📦 Total produits en DB: {len(products['products'])}")

        # Afficher toutes les catégories
        categories = set(p['category'] for p in products['products'])
        print(f"📋 Catégories disponibles: {categories}")

        recommended = [p for p in products['products']
                      if p['category'] == prediction['category']]

        print(f"✅ Produits trouvés pour '{prediction['category']}': {len(recommended)}")

        recommended = recommended[:6]

        return jsonify({
            'statut': 'succes',
            'prediction': prediction,
            'recommended_products': recommended,
            'message': f"Nous vous recommandons les {prediction['category']}"
        }), 200

    except Exception as e:
        import traceback
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        print(f"❌ Erreur: {error_msg}")
        return jsonify({
            'erreur': str(e),
            'statut': 'erreur'
        }), 500
