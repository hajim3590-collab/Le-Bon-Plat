from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from config import DEBUG, PORT
from routes import menu, reviews
import logging
from datetime import datetime
import os
import time

try:
    from routes import recommendations
except ImportError as e:
    print(f"❌ Erreur: Impossible de charger recommendations: {e}")
    print("Vérifiez que backend/models/ml_model.py existe et n'a pas d'erreurs")
    recommendations = None


# ===== SETUP LOGGING =====
os.makedirs('logs', exist_ok=True)
log_file = f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("="*80)
logger.info("APPLICATION LE BON PLAT DEMARREE")
logger.info("="*80)

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# ===== MIDDLEWARE LOGGING =====
@app.before_request
def log_request():
    """Enregistrer chaque requete + marquer le debut"""
    request.start_time = time.time()
    logger.info(f"REQUEST {request.method} {request.path} - IP: {request.remote_addr}")

@app.after_request
def log_response(response):
    """Enregistrer chaque reponse + temps d'execution"""
    if hasattr(request, 'start_time'):
        duration = (time.time() - request.start_time) * 1000
        logger.info(f"RESPONSE {request.method} {request.path} - Status: {response.status_code} - Temps: {duration:.2f}ms")
    else:
        logger.info(f"RESPONSE {request.method} {request.path} - Status: {response.status_code}")
    return response

@app.errorhandler(404)
def handle_404(error):
    """Gerer les erreurs 404"""
    logger.warning(f"404 NOT FOUND: {request.path}")
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(Exception)
def handle_error(error):
    """Gerer les erreurs globalement"""
    logger.error(f"ERREUR: {str(error)}")
    return jsonify({'error': str(error)}), 500
# ===== ENREGISTRER LES ROUTES =====
app.register_blueprint(menu.bp)
app.register_blueprint(reviews.bp)

if recommendations:
    app.register_blueprint(recommendations.bp)

# ===== SERVIR LES FICHIERS FRONTEND =====
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/images/<filename>')
def serve_images(filename):
    return send_from_directory('../frontend/images', filename)

@app.route('/<path:path>')
def serve_files(path):
    return send_from_directory('../frontend', path)

# ===== ROUTES DE TEST =====
@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/status')
def api_status():
    return jsonify({
        'application': 'Le Bon Plat',
        'version': '2.0',
        'status': 'running',
        'endpoints': [
            'GET /api/menu',
            'GET /api/menu/<category>',
            'POST /api/recommendations'
        ]
    })

@app.route('/api/test-recommend')
def test_recommend():
    """Endpoint de test pour vérifier les recommandations"""
    try:
        from models.ml_model import ml
        import json
        from config import PRODUCTS_DB_PATH

        with open(PRODUCTS_DB_PATH, 'r', encoding='utf-8') as f:
            products = json.load(f)

        # Test avec des valeurs fixes
        pred = ml.predict(15, 15, 8, 0)
        categories = set(p['category'] for p in products['products'])
        matching_products = [p for p in products['products'] if p['category'] == pred['category']]

        return jsonify({
            'model_prediction': pred,
            'available_categories': sorted(list(categories)),
            'total_products': len(products['products']),
            'products_in_predicted_category': len(matching_products),
            'matching_products': matching_products[:3]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== LANCER L'APP =====
if __name__ == '__main__':
    print("\n" + "="*80)
    print("API LE BON PLAT v2.0")
    print("="*80)
    print(f"\n🍽️  Application lancée sur http://localhost:{PORT}")
    print("\nEndpoints :")
    print(f"  GET  /                    - Page d'accueil")
    print(f"  GET  /api/menu            - Tous les produits")
    print(f"  GET  /api/menu/<categorie> - Produits par catégorie")
    print(f"  POST /api/recommendations - Recommandations IA")
    print(f"  GET  /api/status          - Statut de l'API")
    print(f"  GET  /health              - Vérification santé")
    print("\n" + "="*80 + "\n")
    
    app.run(debug=DEBUG, port=PORT)