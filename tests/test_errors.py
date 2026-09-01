import json

class TestErrorHandling:
    """Tests pour verifier la gestion des erreurs"""

    def test_404_not_found(self, client):
        """Test: Route inexistante retourne 404"""
        response = client.get('/api/inexistant')
        assert response.status_code == 404

    def test_invalid_json_request(self, client):
        """Test: JSON invalide retourne erreur"""
        response = client.post('/api/reviews',
                              data='INVALID JSON',
                              content_type='application/json')
        # Doit retourner erreur 400 ou 500
        assert response.status_code in [400, 500]

    def test_review_invalid_rating_type(self, client):
        """Test: Rating non valide retourne erreur"""
        review_data = {
            'name': 'Test',
            'rating': 'pas_un_nombre',  # Invalide
            'comment': 'Test'
        }

        response = client.post('/api/reviews',
                              data=json.dumps(review_data),
                              content_type='application/json')

        # Doit retourner erreur
        assert response.status_code in [400, 500]

    def test_review_empty_name(self, client):
        """Test: Avis sans nom retourne erreur 400"""
        review_data = {
            'name': '',  # Nom vide
            'rating': 5,
            'comment': 'Test'
        }

        response = client.post('/api/reviews',
                              data=json.dumps(review_data),
                              content_type='application/json')

        assert response.status_code == 400


class TestCategoryFiltering:
    """Tests pour verifier le filtrage par categorie"""

    def test_invalid_category_name(self, client):
        """Test: Categorie inexistante retourne liste vide"""
        response = client.get('/api/menu/CATEGORIE_INEXISTANTE')
        assert response.status_code == 200
        data = json.loads(response.data)

        # Doit retourner une liste vide
        assert 'products' in data
        assert len(data['products']) == 0

    def test_case_insensitive_category(self, client):
        """Test: Filtrage par categorie insensible a la casse"""
        response_upper = client.get('/api/menu/GRILL')
        response_lower = client.get('/api/menu/grill')
        response_mixed = client.get('/api/menu/Grill')

        data_upper = json.loads(response_upper.data)
        data_lower = json.loads(response_lower.data)
        data_mixed = json.loads(response_mixed.data)

        # Les trois devraient retourner les memes resultats
        assert len(data_upper['products']) == len(data_lower['products'])
        assert len(data_lower['products']) == len(data_mixed['products'])
