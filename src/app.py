from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

print("Chargement du modele...")
model = pickle.load(open('../data/processed/best_model_v3_mois_jour.pkl', 'rb'))
le_category = pickle.load(open('../data/processed/le_category.pkl', 'rb'))
menu_df = pd.read_csv('../data/processed/menu_final_clean.csv')

print("Modele charge avec succes !")
print(f"Categories : {list(le_category.classes_)}")

@app.route('/')
def serve_html():
    return send_file('index.html', mimetype='text/html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        temperature = float(data['temperature_c'])
        budget = float(data['budget'])
        mois = int(data['mois'])
        jour = int(data['jour_semaine'])
        
        X = np.array([[temperature, budget, mois, jour]])
        prediction_encoded = model.predict(X)[0]
        prediction_proba = model.predict_proba(X)[0]
        prediction_label = le_category.inverse_transform([prediction_encoded])[0]
        
        plats = menu_df[menu_df['category'] == prediction_label]
        
        return jsonify({
            'statut': 'succes',
            'contexte': {
                'temperature': temperature,
                'budget': budget,
                'mois': mois,
                'jour_semaine': jour
            },
            'prediction': {
                'categorie': prediction_label,
                'confiance': float(prediction_proba.max()),
                'probabilites': {
                    le_category.inverse_transform([i])[0]: float(prediction_proba[i])
                    for i in range(len(le_category.classes_))
                }
            },
            'plats_recommandes': plats[['dish_name', 'category']].to_dict('records')
        }), 200
    
    except Exception as e:
        return jsonify({'erreur': str(e), 'statut': 'erreur'}), 500

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'modele': 'Random Forest',
        'accuracy': '90.52%',
        'features': ['temperature_c', 'budget', 'mois', 'jour_semaine'],
        'categories': list(le_category.classes_)
    })

if __name__ == '__main__':
    print("\n" + "="*80)
    print("API LE BON PLAT sur http://localhost:5000")
    print("="*80 + "\n")
    app.run(debug=True, port=5000)