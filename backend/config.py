import os

# Chemins des fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, '..', 'data', 'processed')

# Chemins des fichiers ML
ML_MODEL_PATH = os.path.join(MODELS_DIR, 'best_model_v3_mois_jour.pkl')
LE_CATEGORY_PATH = os.path.join(MODELS_DIR, 'le_category.pkl')

# Chemin de la base de données produits
PRODUCTS_DB_PATH = os.path.join(DATA_DIR, 'products_db.json')

# Chemin de la base de données avis
REVIEWS_DB_PATH = os.path.join(DATA_DIR, 'reviews.json')

# Configuration Flask
DEBUG = True
PORT = 5000