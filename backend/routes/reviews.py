from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime
from config import REVIEWS_DB_PATH

bp = Blueprint('reviews', __name__, url_prefix='/api')

@bp.route('/reviews', methods=['GET'])
def get_reviews():
    """Récupérer tous les avis"""
    try:
        with open(REVIEWS_DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({
            'reviews': data.get('reviews', []),
            'count': len(data.get('reviews', []))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reviews', methods=['POST'])
def add_review():
    """Ajouter un nouvel avis"""
    try:
        data = request.get_json()

        # Valider les données
        if not data.get('name') or not data.get('rating') or not data.get('comment'):
            return jsonify({'error': 'Nom, note et commentaire requis'}), 400

        # Charger les avis existants
        with open(REVIEWS_DB_PATH, 'r', encoding='utf-8') as f:
            reviews_data = json.load(f)

        # Ajouter le nouvel avis
        new_review = {
            'id': len(reviews_data['reviews']) + 1,
            'name': data['name'],
            'rating': int(data['rating']),
            'comment': data['comment'],
            'date': datetime.now().strftime('%d/%m/%Y %H:%M')
        }

        reviews_data['reviews'].append(new_review)

        # Sauvegarder
        with open(REVIEWS_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(reviews_data, f, indent=2, ensure_ascii=False)

        return jsonify({
            'message': 'Avis ajouté avec succès!',
            'review': new_review
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
