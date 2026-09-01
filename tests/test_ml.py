import sys
import os
import pickle
import numpy as np

# Ajouter le chemin backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from config import ML_MODEL_PATH, LE_CATEGORY_PATH

class TestMLModel:
    """Tests du modele Machine Learning"""

    def test_model_file_exists(self):
        """Test: Le fichier du modele existe"""
        assert os.path.exists(ML_MODEL_PATH), f"Modele non trouve: {ML_MODEL_PATH}"

    def test_label_encoder_file_exists(self):
        """Test: Le fichier LabelEncoder existe"""
        assert os.path.exists(LE_CATEGORY_PATH), f"LabelEncoder non trouve: {LE_CATEGORY_PATH}"

    def test_model_can_be_loaded(self):
        """Test: Le modele peut etre charge"""
        try:
            with open(ML_MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            assert model is not None
        except Exception as e:
            raise AssertionError(f"Erreur lors du chargement du modele: {e}")

    def test_label_encoder_can_be_loaded(self):
        """Test: LabelEncoder peut etre charge"""
        try:
            with open(LE_CATEGORY_PATH, 'rb') as f:
                le = pickle.load(f)
            assert le is not None
        except Exception as e:
            raise AssertionError(f"Erreur lors du chargement du LabelEncoder: {e}")

    def test_model_prediction_shape(self):
        """Test: Le modele retourne une prediction valide"""
        try:
            with open(ML_MODEL_PATH, 'rb') as f:
                model = pickle.load(f)

            # Donnees de test
            X_test = np.array([[15, 15, 8, 2]])  # budget, preference, mois, jour

            prediction = model.predict(X_test)

            # Vérifier structure
            assert prediction is not None
            assert len(prediction) == 1
            assert isinstance(prediction[0], (np.int64, np.int32, int))

        except Exception as e:
            raise AssertionError(f"Erreur lors de la prediction: {e}")

    def test_model_probability_prediction(self):
        """Test: Le modele retourne des probabilites"""
        try:
            with open(ML_MODEL_PATH, 'rb') as f:
                model = pickle.load(f)

            X_test = np.array([[15, 15, 8, 2]])

            # Verifier que predict_proba existe
            if hasattr(model, 'predict_proba'):
                probas = model.predict_proba(X_test)
                assert probas is not None
                assert len(probas) == 1
                # Les probabilites doivent etre entre 0 et 1
                assert np.all((probas >= 0) & (probas <= 1))

        except Exception as e:
            raise AssertionError(f"Erreur lors de la prediction de probabilites: {e}")


class TestMLIntegration:
    """Tests d'integration du modele ML"""

    def test_recommendations_api_with_valid_data(self, client):
        """Test: API recommendations avec donnees valides"""
        recommendation_data = {
            'budget': 15,
            'preference': 15,
            'mois': 8,
            'jour': 2
        }

        response = client.post('/api/recommendations',
                              data='{"budget": 15, "preference": 15, "mois": 8, "jour": 2}',
                              content_type='application/json')

        # Doit retourner 200 ou 201
        assert response.status_code in [200, 201]

    def test_recommendations_api_returns_valid_category(self, client):
        """Test: API recommendations retourne une categorie valide"""
        response = client.post('/api/recommendations',
                              data='{"budget": 15, "preference": 15, "mois": 8, "jour": 2}',
                              content_type='application/json')

        assert response.status_code in [200, 201]

        import json
        data = json.loads(response.data)

        # Verifier qu'une categorie est retournee
        assert 'category' in data or 'prediction' in data or 'recommended_category' in data
