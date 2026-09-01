import csv

# Ouvrir le fichier
with open('sales_history.csv', 'r') as f:
    reader = csv.DictReader(f)
    
    # Compter les lignes
    lignes = list(reader)
    print(f"Nombre de lignes : {len(lignes)}")
    
    # Afficher les colonnes
    if lignes:
        print(f"Colonnes : {list(lignes[0].keys())}")
        print(f"\nPremière ligne :")
        print(lignes[0])

        
# Charger menu_database_export.csv
with open('menu_database_export.csv', 'r') as f:
    reader = csv.DictReader(f)
    menu_db = list(reader)
    print(f"\nMenu Database : {len(menu_db)} plats")
    print(f"Colonnes : {list(menu_db[0].keys())}")
    print(f"Premier plat : {menu_db[0]}")


    # Charger menu_fournisseur.csv
with open('menu_fournisseur.csv', 'r') as f:
    reader = csv.DictReader(f)
    menu_fournisseur = list(reader)
    print(f"\nMenu Fournisseur : {len(menu_fournisseur)} plats")
    print(f"Colonnes : {list(menu_fournisseur[0].keys())}")
    print(f"Premier plat : {menu_fournisseur[0]}")

# Charger menu_site_web.json
import json
with open('menu_site_web.json', 'r') as f:
    data_json = json.load(f)
    menu_web = data_json['plats']
    print(f"\nMenu Site Web : {len(menu_web)} plats")
    print(f"Colonnes : {list(menu_web[0].keys())}")
    print(f"Premier plat : {menu_web[0]}")

    # Charger competitor_prices.csv
with open('competitor_prices.csv', 'r') as f:
    reader = csv.DictReader(f)
    competitor_prices = list(reader)
    print(f"\nCompetitor Prices : {len(competitor_prices)} lignes")
    print(f"Colonnes : {list(competitor_prices[0].keys())}")
    print(f"Première ligne : {competitor_prices[0]}")

# Charger weather_forecast.json
with open('weather_forecast.json', 'r') as f:
    data_json = json.load(f)
    weather = data_json['forecast']
    print(f"\nWeather Forecast : {len(weather)} jours")
    print(f"Colonnes : {list(weather[0].keys())}")
    print(f"Premier jour : {weather[0]}")