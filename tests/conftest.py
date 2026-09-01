import pytest
import sys
import os

# Ajouter le dossier backend au chemin
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app as flask_app

@pytest.fixture
def app():
    """Configuration de l'app Flask pour les tests"""
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    """Client Flask pour faire des requetes dans les tests"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI runner pour tester les commandes"""
    return app.test_cli_runner()
