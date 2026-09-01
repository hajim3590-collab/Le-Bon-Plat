import pandas as pd

# Ouvrir le fichier menu_fournisseur.csv
df = pd.read_csv('../data/raw/menu_fournisseur.csv')

# Afficher le tableau complet
print("=== CONTENU DU FICHIER ===")
print(df)

# Afficher les informations du fichier
print("\n=== STRUCTURE DU FICHIER ===")
print(df.info())

# Afficher les statistiques
print("\n=== STATISTIQUES ===")
print(df.describe())
print("\n=== NETTOYAGE ===")

# Problème 1 : Supprimer la ligne "Plat mystere" (pas de catégorie)
df = df[df['dish_name'] != 'Plat mystere']
print(f"✓ Suppression de 'Plat mystere'")

# Problème 2 : Remplacer le prix manquant du Fondant chocolat par 7.00 (trouvé dans menu_site_web.json)
df.loc[df['dish_name'] == 'Fondant chocolat', 'price'] = 7.0
print(f"✓ Prix du Fondant chocolat remplacé par 7.0")

# Problème 3 : Supprimer la ligne "Salade complete" (currency = "none", plat suspect)
df = df[df['dish_name'] != 'Salade complete']
print(f"✓ Suppression de 'Salade complete'")

# Corriger la devise "none" en "EUR"
df['currency'] = df['currency'].replace('none', 'EUR')
print(f"✓ Devise corrigée")

# Afficher le résultat
print("\n=== FICHIER NETTOYÉ ===")
print(df)
# Sauvegarder le fichier nettoyé
df.to_csv('../data/processed/menu_fournisseur_clean.csv', index=False)
print("\n✓ Fichier sauvegardé dans data/processed/menu_fournisseur_clean.csv")

print("\n\n" + "="*50)
print("=== FICHIER 2 : MENU DATABASE ===")
print("="*50)

# Charger le fichier
df_db = pd.read_csv('../data/raw/menu_database_export.csv')

# Afficher le contenu
print("\n=== CONTENU DU FICHIER ===")
print(df_db)

# Afficher la structure
print("\n=== STRUCTURE DU FICHIER ===")
print(df_db.info())

# Afficher les statistiques
print("\n=== STATISTIQUES ===")
print(df_db.describe())

print("\n=== NETTOYAGE MENU DATABASE ===")

# Renommer les colonnes pour qu'elles correspondent aux autres sources
df_db = df_db.rename(columns={
    'item_name': 'dish_name',
    'category_code': 'category',
    'price_cents': 'price'
})

# Traduire les codes de catégories en texte complet
category_map = {
    'ENT': 'Entree',
    'PDJ': 'Plat_du_jour',
    'GRL': 'Grill',
    'VEG': 'Vegetarien',
    'DES': 'Dessert',
    'ENF': 'Enfant'
}
df_db['category'] = df_db['category'].map(category_map)
print(f"✓ Catégories traduites")

# Convertir les prix de cents en euros
df_db['price'] = df_db['price'] / 100
print(f"✓ Prix convertis en euros")

# Ajouter la devise et la source
df_db['currency'] = 'EUR'
df_db['source'] = 'database'

# Supprimer les colonnes inutiles (item_id, is_active)
df_db = df_db.drop(columns=['item_id', 'is_active'])

# Afficher le résultat
print("\n=== FICHIER NETTOYÉ ===")
print(df_db)

# Sauvegarder
df_db.to_csv('../data/processed/menu_database_clean.csv', index=False)
print("\n✓ Fichier sauvegardé dans data/processed/menu_database_clean.csv")

print("\n\n" + "="*50)
print("=== FICHIER 3 : MENU SITE WEB ===")
print("="*50)

# Charger le fichier JSON
import json
with open('../data/raw/menu_site_web.json', 'r') as f:
    data_json = json.load(f)

# Extraire les plats (c'est dans la clé 'plats')
df_web = pd.DataFrame(data_json['plats'])

# Afficher le contenu
print("\n=== CONTENU DU FICHIER ===")
print(df_web)

# Afficher la structure
print("\n=== STRUCTURE DU FICHIER ===")
print(df_web.info())

# Afficher les statistiques
print("\n=== STATISTIQUES ===")
print(df_web.describe())

print("\n=== NETTOYAGE MENU SITE WEB ===")

# Renommer les colonnes
df_web = df_web.rename(columns={
    'nom': 'dish_name',
    'categorie': 'category',
    'prix': 'price'
})
print(f"✓ Colonnes renommées")

# Normaliser les catégories
category_map_web = {
    'Entrees': 'Entree',
    'Plats': 'Plat_du_jour',
    'Grillades': 'Grill',
    'Vege': 'Vegetarien',
    'Desserts': 'Dessert',
    'Enfants': 'Enfant'
}
df_web['category'] = df_web['category'].map(category_map_web)
print(f"✓ Catégories normalisées")

# Convertir les prix : "8,50 e" → 8.5
# 1. Supprimer le " e" à la fin
df_web['price'] = df_web['price'].str.replace(' e', '')
# 2. Remplacer la virgule par un point
df_web['price'] = df_web['price'].str.replace(',', '.')
# 3. Convertir en nombre décimal
df_web['price'] = df_web['price'].astype(float)
print(f"✓ Prix convertis en nombres")

# Ajouter la devise et la source
df_web['currency'] = 'EUR'
df_web['source'] = 'web'

# Afficher le résultat
print("\n=== FICHIER NETTOYÉ ===")
print(df_web)

# Sauvegarder
df_web.to_csv('../data/processed/menu_site_web_clean.csv', index=False)
print("\n✓ Fichier sauvegardé dans data/processed/menu_site_web_clean.csv")

print("\n\n" + "="*50)
print("=== FICHIER 4 : COMPETITOR PRICES ===")
print("="*50)

# Charger le fichier
df_comp = pd.read_csv('../data/raw/competitor_prices.csv')

# Afficher le contenu
print("\n=== CONTENU DU FICHIER ===")
print(df_comp)

# Afficher la structure
print("\n=== STRUCTURE DU FICHIER ===")
print(df_comp.info())

# Afficher les statistiques
print("\n=== STATISTIQUES ===")
print(df_comp.describe())
print("\n=== NETTOYAGE COMPETITOR PRICES ===")

# Supprimer les lignes avec dish_name manquant
df_comp = df_comp.dropna(subset=['dish_name'])
print(f"✓ Ligne avec dish_name manquant supprimée")

# Supprimer les lignes avec price manquant
df_comp = df_comp.dropna(subset=['price'])
print(f"✓ Lignes avec price manquant supprimées")

# Standardiser les devises en EUR (majuscules)
df_comp['currency'] = df_comp['currency'].str.upper()
df_comp['currency'] = df_comp['currency'].replace('NONE', 'EUR')
print(f"✓ Devises standardisées en EUR")

# Ajouter la source
df_comp['source'] = 'competitor'

# Afficher le résultat
print("\n=== FICHIER NETTOYÉ ===")
print(df_comp)

# Sauvegarder
df_comp.to_csv('../data/processed/competitor_prices_clean.csv', index=False)
print("\n✓ Fichier sauvegardé dans data/processed/competitor_prices_clean.csv")
print("\n\n" + "="*50)
print("=== FICHIER 5 : SALES HISTORY ===")
print("="*50)

# Charger le fichier
df_sales = pd.read_csv('../data/raw/sales_history.csv')

# Afficher les premières lignes
print("\n=== PREMIÈRES LIGNES ===")
print(df_sales.head(10))

# Afficher la structure
print("\n=== STRUCTURE DU FICHIER ===")
print(df_sales.info())

# Afficher les statistiques
print("\n=== STATISTIQUES ===")
print(df_sales.describe())

# Vérifier les valeurs manquantes
print("\n=== VALEURS MANQUANTES ===")
print(df_sales.isnull().sum())

print("\n=== ANALYSE APPROFONDIE ===")

# Quelles sont les catégories uniques ?
print("\n--- Catégories de plats ---")
print(df_sales['dish_category'].unique())
print(f"Nombre de catégories : {df_sales['dish_category'].nunique()}")

# Quels sont les jours de la semaine ?
print("\n--- Jours de la semaine ---")
print(df_sales['jour_semaine'].unique())

# Y a-t-il des budgets négatifs ou anormaux ?
print("\n--- Budgets anormaux ---")
print(f"Budget min : {df_sales['budget'].min()}")
print(f"Budget max : {df_sales['budget'].max()}")

# Vérifier la plage de température
print("\n--- Température ---")
print(f"Température min : {df_sales['temperature_c'].min()}")
print(f"Température max : {df_sales['temperature_c'].max()}")

print("\n=== NETTOYAGE SALES HISTORY ===")

# Renommer "Menu_Enfant" en "Enfant"
df_sales['dish_category'] = df_sales['dish_category'].replace('Menu_Enfant', 'Enfant')
print(f"✓ 'Menu_Enfant' renommé en 'Enfant'")

# Convertir les dates en datetime
df_sales['date'] = pd.to_datetime(df_sales['date'])
print(f"✓ Dates converties en format datetime")

# Nettoyer les espaces inutiles dans les colonnes texte
df_sales['jour_semaine'] = df_sales['jour_semaine'].str.strip()
df_sales['dish_category'] = df_sales['dish_category'].str.strip()
print(f"✓ Espaces inutiles supprimés")

# Afficher le résultat
print("\n=== FICHIER NETTOYÉ ===")
print(df_sales.head(10))
print(f"\nTotal de lignes : {len(df_sales)}")

# Vérifier les types de données
print("\n=== TYPES DE DONNÉES ===")
print(df_sales.info())

# Sauvegarder
df_sales.to_csv('../data/processed/sales_history_clean.csv', index=False)
print("\n✓ Fichier sauvegardé dans data/processed/sales_history_clean.csv")


print("\n\n" + "="*50)
print("=== FICHIER 6 : WEATHER FORECAST ===")
print("="*50)

# Charger le fichier JSON
with open('../data/raw/weather_forecast.json', 'r') as f:
    data_weather = json.load(f)

# Extraire les prévisions (clé 'forecast')
df_weather = pd.DataFrame(data_weather['forecast'])

# Afficher le contenu
print("\n=== CONTENU DU FICHIER ===")
print(df_weather)

# Afficher la structure
print("\n=== STRUCTURE DU FICHIER ===")
print(df_weather.info())

# Afficher les statistiques
print("\n=== STATISTIQUES ===")
print(df_weather.describe())

# Vérifier les valeurs manquantes
print("\n=== VALEURS MANQUANTES ===")
print(df_weather.isnull().sum())

print("\n=== NETTOYAGE WEATHER FORECAST ===")

# Convertir les dates en datetime
df_weather['date'] = pd.to_datetime(df_weather['date'])
print(f"✓ Dates converties en format datetime")

# Afficher le résultat
print("\n=== FICHIER NETTOYÉ ===")
print(df_weather)

# Vérifier les types
print("\n=== TYPES DE DONNÉES ===")
print(df_weather.info())

# Sauvegarder
df_weather.to_csv('../data/processed/weather_forecast_clean.csv', index=False)
print("\n✓ Fichier sauvegardé dans data/processed/weather_forecast_clean.csv")

print("\n\n" + "="*50)
print("=== CRÉATION : Fichier de Boissons ===")
print("="*50)

# Créer une liste de boissons
beverages_data = [
    {"drink_name": "Coca Cola", "category": "Soda", "price": 2.5, "size_ml": 330, "is_available": 1},
    {"drink_name": "Fanta Orange", "category": "Soda", "price": 2.3, "size_ml": 330, "is_available": 1},
    {"drink_name": "Dada", "category": "Soda", "price": 2.0, "size_ml": 330, "is_available": 1},
    {"drink_name": "Sprite", "category": "Soda", "price": 2.5, "size_ml": 330, "is_available": 1},
    {"drink_name": "Hawi", "category": "Boisson Energisante", "price": 3.0, "size_ml": 250, "is_available": 1},
    {"drink_name": "Oasis", "category": "Jus/Nectar", "price": 2.8, "size_ml": 330, "is_available": 1},
    {"drink_name": "Eau Minerale", "category": "Eau", "price": 1.5, "size_ml": 500, "is_available": 1},
    {"drink_name": "Jus d'Orange Frais", "category": "Jus Frais", "price": 3.5, "size_ml": 250, "is_available": 1},
    {"drink_name": "Pepsi", "category": "Soda", "price": 2.3, "size_ml": 330, "is_available": 1},
    {"drink_name": "Orangena", "category": "Jus/Nectar", "price": 2.5, "size_ml": 330, "is_available": 1},
    {"drink_name": "Jus de Pomme", "category": "Jus/Nectar", "price": 2.8, "size_ml": 250, "is_available": 1},
    {"drink_name": "The Glace", "category": "Boisson Chaude", "price": 2.2, "size_ml": 250, "is_available": 0},
]

# Créer un DataFrame
df_beverages = pd.DataFrame(beverages_data)

print("\n=== FICHIER BOISSONS ===")
print(df_beverages)

# Sauvegarder
df_beverages.to_csv('../data/raw/beverages.csv', index=False)
print("\n✓ Fichier sauvegardé dans data/raw/beverages.csv")

print("\n\n" + "="*50)
print("=== FICHIER 7 : BEVERAGES ===")
print("="*50)

# Charger le fichier
df_bev = pd.read_csv('../data/raw/beverages.csv')

# Afficher le contenu
print("\n=== CONTENU DU FICHIER ===")
print(df_bev)

# Afficher la structure
print("\n=== STRUCTURE DU FICHIER ===")
print(df_bev.info())

# Afficher les statistiques
print("\n=== STATISTIQUES ===")
print(df_bev.describe())

# Vérifier les valeurs manquantes
print("\n=== VALEURS MANQUANTES ===")
print(df_bev.isnull().sum())

# Analyser les catégories
print("\n=== CATÉGORIES UNIQUES ===")
print(df_bev['category'].unique())
print("\n=== NETTOYAGE BEVERAGES ===")

# Charger le fichier
df_bev = pd.read_csv('../data/raw/beverages.csv')

# Nettoyer les espaces inutiles dans les noms et catégories
df_bev['drink_name'] = df_bev['drink_name'].str.strip()
df_bev['category'] = df_bev['category'].str.strip()
print(f"✓ Espaces inutiles supprimés")

# Ajouter la source
df_bev['source'] = 'beverages'
print(f"✓ Colonne 'source' ajoutée")

# Afficher le résultat
print("\n=== FICHIER NETTOYÉ ===")
print(df_bev)

# Sauvegarder
df_bev.to_csv('../data/processed/beverages_clean.csv', index=False)
print("\n✓ Fichier sauvegardé dans data/processed/beverages_clean.csv")