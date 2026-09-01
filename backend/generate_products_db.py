import pandas as pd
import json
import os

# Lire les plats
df_plats = pd.read_csv('../data/processed/menu_final_clean.csv')

# Lire les boissons (si elles existent)
try:
    df_boissons = pd.read_csv('../data/raw/beverages.csv')
    has_boissons = True
except FileNotFoundError:
    has_boissons = False
    print("⚠️  Fichier beverages.csv non trouvé, on crée juste les plats")

# Créer la liste des produits
products = []
id_counter = 1

# Ajouter les plats
for idx, row in df_plats.iterrows():
    product = {
        "id": id_counter,
        "name": row['dish_name'],
        "category": row['category'],
        "price": float(row['price']) if pd.notna(row['price']) else 0.0,
        "description": f"Délicieux {row['dish_name'].lower()}",
        "image": "https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=400"
    }
    products.append(product)
    id_counter += 1

# Ajouter les boissons si le fichier existe
if has_boissons:
    for idx, row in df_boissons.iterrows():
        product = {
            "id": id_counter,
            "name": row.get('beverage_name', row.get('name', 'Boisson')),
            "category": "Boissons",
            "price": float(row.get('price', 2.50)) if pd.notna(row.get('price', 2.50)) else 2.50,
            "description": f"Boisson rafraîchissante",
            "image": "https://images.unsplash.com/photo-1554866585-acbb2231f1d7?w=400"
        }
        products.append(product)
        id_counter += 1

# Créer le JSON
output = {"products": products}

# Sauvegarder
output_path = 'data/products_db.json'
os.makedirs('data', exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"✅ {len(products)} produits importés dans {output_path}")
print(f"\nProduits créés :")
for p in products:
    print(f"  {p['id']:2d}. {p['name']:30s} ({p['category']:15s}) {p['price']:6.2f}€")