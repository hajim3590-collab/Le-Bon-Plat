import json

class TestAPIBasic:
    """Tests des routes API de base"""

    def test_health_endpoint(self, client):
        """Test: GET /health retourne status ok"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'

    def test_api_status(self, client):
        """Test: GET /api/status retourne info app"""
        response = client.get('/api/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['application'] == 'Le Bon Plat'
        assert data['status'] == 'running'
        assert data['version'] == '2.0'


class TestMenuAPI:
    """Tests de la route menu"""

    def test_get_all_products(self, client):
        """Test: GET /api/menu retourne tous les produits"""
        response = client.get('/api/menu')
        assert response.status_code == 200
        data = json.loads(response.data)

        # Vérifier structure
        assert 'products' in data
        assert isinstance(data['products'], list)
        assert len(data['products']) > 0

    def test_get_products_by_category(self, client):
        """Test: GET /api/menu/<category> retourne produits d'une categorie"""
        response = client.get('/api/menu/Grill')
        assert response.status_code == 200
        data = json.loads(response.data)

        # Vérifier structure
        assert 'products' in data
        assert isinstance(data['products'], list)

        # Vérifier que les produits sont de la bonne catégorie
        for product in data['products']:
            assert product['category'].lower() == 'grill'

    def test_product_structure(self, client):
        """Test: Chaque produit a la bonne structure"""
        response = client.get('/api/menu')
        data = json.loads(response.data)

        for product in data['products']:
            # Vérifier que chaque produit a les champs requis
            assert 'id' in product
            assert 'name' in product
            assert 'category' in product
            assert 'price' in product
            assert 'description' in product


class TestReviewsAPI:
    """Tests de la route reviews"""

    def test_get_reviews(self, client):
        """Test: GET /api/reviews retourne les avis"""
        response = client.get('/api/reviews')
        assert response.status_code == 200
        data = json.loads(response.data)

        # Vérifier structure
        assert 'reviews' in data
        assert 'count' in data
        assert isinstance(data['reviews'], list)
        assert isinstance(data['count'], int)

    def test_post_review_success(self, client):
        """Test: POST /api/reviews ajoute un avis"""
        review_data = {
            'name': 'Test User',
            'rating': 5,
            'comment': 'Tres bon service!'
        }

        response = client.post('/api/reviews',
                              data=json.dumps(review_data),
                              content_type='application/json')

        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'review' in data
        assert data['review']['name'] == 'Test User'
        assert data['review']['rating'] == 5

    def test_post_review_missing_fields(self, client):
        """Test: POST /api/reviews sans tous les champs → Erreur 400"""
        review_data = {
            'name': 'Test User'
            # Manque 'rating' et 'comment'
        }

        response = client.post('/api/reviews',
                              data=json.dumps(review_data),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestRecommendationsAPI:
    """Tests de la route recommendations"""

    def test_recommendations_endpoint_exists(self, client):
        """Test: POST /api/recommendations existe"""
        recommendation_data = {
            'budget': 15,
            'preference': 10,
            'mois': 8,
            'jour': 2
        }

        response = client.post('/api/recommendations',
                              data=json.dumps(recommendation_data),
                              content_type='application/json')

        # Accepte 200 ou 201
        assert response.status_code in [200, 201]
        data = json.loads(response.data)

        # Vérifier structure
        assert 'category' in data or 'prediction' in data or 'recommended_category' in data
