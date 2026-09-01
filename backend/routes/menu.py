from flask import Blueprint, jsonify
from config import PRODUCTS_DB_PATH
import json

bp = Blueprint('menu', __name__, url_prefix='/api')

# Charger les produits du fichier JSON
def load_products():
    with open(PRODUCTS_DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# Route : retourner TOUS les produits
@bp.route('/menu', methods=['GET'])
def get_all_products():
    products = load_products()
    return jsonify(products)

# Route : retourner produits d'UNE catégorie
@bp.route('/menu/<category>', methods=['GET'])
def get_products_by_category(category):
    products = load_products()
    filtered = [p for p in products['products'] if p['category'].lower() == category.lower()]
    return jsonify({'products': filtered})