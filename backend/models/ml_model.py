import pickle
import numpy as np
import sys
import os

# Importer config du répertoire parent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ML_MODEL_PATH, LE_CATEGORY_PATH

class MLModel:
    """Classe qui charge le modèle ML et fait des prédictions"""
    
    def __init__(self):
        """Charger le modèle une seule fois au démarrage"""
        print("Chargement du modèle ML...")
        self.model = pickle.load(open(ML_MODEL_PATH, 'rb'))
        self.le_category = pickle.load(open(LE_CATEGORY_PATH, 'rb'))
        print("Modèle chargé !")
    
    def predict(self, temperature, budget, month, day):
        """
        Faire une prédiction
        
        Entrées :
            temperature (float) : Température en °C
            budget (float) : Budget en euros
            month (int) : Mois (1-12)
            day (int) : Jour (0=Lundi, 6=Dimanche)
        
        Retour :
            dict : {'category': 'Plat_du_jour', 'confidence': 0.92}
        """
        # Préparer les données pour le modèle
        X = np.array([[temperature, budget, month, day]])
        
        # Le modèle prédit
        prediction_encoded = self.model.predict(X)[0]
        prediction_proba = self.model.predict_proba(X)[0]
        
        # Convertir le nombre en catégorie
        category = self.le_category.inverse_transform([prediction_encoded])[0]
        confidence = float(prediction_proba.max())
        
        return {
            'category': category,
            'confidence': confidence
        }

# Créer une instance globale
ml = MLModel()