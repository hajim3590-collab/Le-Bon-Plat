import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import time

print("="*80)
print("=== ENTRAÎNEMENT DES MODÈLES (AVEC MOIS + JOUR) ===")
print("="*80)

# ===== ÉTAPE 1 : Charger et préparer les données =====
print("\n--- CHARGEMENT DES DONNÉES ---")

df = pd.read_csv('data/processed/sales_history_clean.csv')
df_menu = pd.read_csv('data/processed/menu_final_clean.csv')

# Fusionner les données
df_sales_menu = df.merge(df_menu[['dish_name', 'category']], left_on='dish_category', right_on='category', how='left')

print(f"Total de commandes : {len(df_sales_menu)}")

# ===== ÉTAPE 2 : Extraire le MOIS et le JOUR =====
print("\n--- EXTRACTION DU MOIS ET DU JOUR ---")

# Convertir la date en datetime
df_sales_menu['date'] = pd.to_datetime(df_sales_menu['date'])

# Extraire le mois (1-12)
df_sales_menu['mois'] = df_sales_menu['date'].dt.month

# Extraire le jour de la semaine (0=Lundi, 6=Dimanche)
df_sales_menu['jour_semaine'] = df_sales_menu['date'].dt.dayofweek

print(f"\nExemple d'extractions :")
print(df_sales_menu[['date', 'mois', 'jour_semaine']].head(10))

# ===== ÉTAPE 3 : Préparer les features (X) et la cible (y) =====
print("\n--- PRÉPARATION DES FEATURES ---")

# Features : température, budget, MOIS, JOUR
X = df_sales_menu[['temperature_c', 'budget', 'mois', 'jour_semaine']].copy()
y = df_sales_menu['dish_category'].copy()

print(f"Features (X) : {X.columns.tolist()}")
print(f"Cible (y) : {y.name}")
print(f"Nombre d'exemples : {len(X)}")
print(f"\nStatistiques des features :")
print(X.describe())

# ===== ÉTAPE 4 : Encoder la cible =====
le_category = LabelEncoder()
y_encoded = le_category.fit_transform(y)

print(f"\nCatégories encodées : {dict(zip(le_category.classes_, le_category.transform(le_category.classes_)))}")

# ===== ÉTAPE 5 : Diviser en train et test =====
print("\n--- DIVISION TRAIN/TEST ---")

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print(f"Données d'entraînement : {len(X_train)} exemples")
print(f"Données de test : {len(X_test)} exemples")
print(f"Ratio train/test : {len(X_train)/(len(X_train)+len(X_test))*100:.1f}% / {len(X_test)/(len(X_train)+len(X_test))*100:.1f}%")

# ===== ÉTAPE 6 : Définir les modèles =====
print("\n" + "="*80)
print("=== ENTRAÎNEMENT ET ÉVALUATION DES MODÈLES (MOIS + JOUR) ===")
print("="*80)

models = {
    'Naive Bayes': GaussianNB(),
    'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=10),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10),
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
}

results = {}

# ===== ÉTAPE 7 : Entraîner et évaluer chaque modèle =====
for model_name, model in models.items():
    print(f"\n{'='*80}")
    print(f"MODÈLE : {model_name}")
    print(f"{'='*80}")

    # Entraîner
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time

    # Prédire
    y_pred = model.predict(X_test)

    # Évaluer
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    results[model_name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'training_time': training_time,
        'model': model,
        'y_pred': y_pred
    }

    print(f"\nAccuracy  : {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1-Score  : {f1:.4f}")
    print(f"Temps d'entraînement : {training_time:.4f}s")

# ===== ÉTAPE 8 : Créer un tableau comparatif =====
print("\n\n" + "="*80)
print("=== TABLEAU COMPARATIF (MOIS + JOUR) ===")
print("="*80)

comparison_df = pd.DataFrame({
    'Modèle': list(results.keys()),
    'Accuracy': [results[m]['accuracy'] for m in results.keys()],
    'Precision': [results[m]['precision'] for m in results.keys()],
    'Recall': [results[m]['recall'] for m in results.keys()],
    'F1-Score': [results[m]['f1'] for m in results.keys()],
    'Temps (s)': [results[m]['training_time'] for m in results.keys()]
})

comparison_df = comparison_df.round(4)
print("\n")
print(comparison_df.to_string(index=False))

# Sauvegarder le tableau
comparison_df.to_csv('data/processed/modeles_comparaison_v3_mois_jour.csv', index=False)
print("\n✓ Tableau sauvegardé : modeles_comparaison_v3_mois_jour.csv")

# ===== ÉTAPE 9 : Créer des graphiques comparatifs =====
print("\n--- CRÉATION DES GRAPHIQUES ---")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Comparaison Des Modèles (MOIS + JOUR)', fontsize=14, fontweight='bold')

# Accuracy
ax1 = axes[0, 0]
ax1.bar(comparison_df['Modèle'], comparison_df['Accuracy'], color='steelblue')
ax1.set_ylabel('Accuracy')
ax1.set_title('Accuracy Par Modèle')
ax1.set_ylim([0, 1])
for i, v in enumerate(comparison_df['Accuracy']):
    ax1.text(i, v + 0.02, f'{v:.3f}', ha='center')
ax1.tick_params(axis='x', rotation=45)

# Precision
ax2 = axes[0, 1]
ax2.bar(comparison_df['Modèle'], comparison_df['Precision'], color='coral')
ax2.set_ylabel('Precision')
ax2.set_title('Precision Par Modèle')
ax2.set_ylim([0, 1])
for i, v in enumerate(comparison_df['Precision']):
    ax2.text(i, v + 0.02, f'{v:.3f}', ha='center')
ax2.tick_params(axis='x', rotation=45)

# F1-Score
ax3 = axes[1, 0]
ax3.bar(comparison_df['Modèle'], comparison_df['F1-Score'], color='lightgreen')
ax3.set_ylabel('F1-Score')
ax3.set_title('F1-Score Par Modèle')
ax3.set_ylim([0, 1])
for i, v in enumerate(comparison_df['F1-Score']):
    ax3.text(i, v + 0.02, f'{v:.3f}', ha='center')
ax3.tick_params(axis='x', rotation=45)

# Temps d'entraînement
ax4 = axes[1, 1]
ax4.bar(comparison_df['Modèle'], comparison_df['Temps (s)'], color='gold')
ax4.set_ylabel('Temps (secondes)')
ax4.set_title('Temps d\'Entraînement')
for i, v in enumerate(comparison_df['Temps (s)']):
    ax4.text(i, v + 0.0001, f'{v:.4f}s', ha='center', fontsize=9)
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('data/processed/modeles_comparaison_v3_mois_jour.png', dpi=100, bbox_inches='tight')
print("✓ Graphique comparatif sauvegardé : modeles_comparaison_v3_mois_jour.png")
plt.show()

# ===== ÉTAPE 10 : Identifier le meilleur modèle =====
print("\n\n" + "="*80)
print("=== MEILLEUR MODÈLE (MOIS + JOUR) ===")
print("="*80)

best_model_name = comparison_df.loc[comparison_df['Accuracy'].idxmax(), 'Modèle']
best_accuracy = comparison_df.loc[comparison_df['Accuracy'].idxmax(), 'Accuracy']

print(f"\n🏆 MEILLEUR MODÈLE : {best_model_name}")
print(f"   Accuracy : {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")

# Sauvegarder le meilleur modèle
import pickle
best_model = results[best_model_name]['model']
pickle.dump(best_model, open('data/processed/best_model_v3_mois_jour.pkl', 'wb'))
print("\n✓ Meilleur modèle sauvegardé : best_model_v3_mois_jour.pkl")

# Sauvegarder les encodeurs aussi
pickle.dump(le_category, open('data/processed/le_category.pkl', 'wb'))
print("✓ Encodeurs sauvegardés : le_category.pkl")

# ===== ÉTAPE 11 : Confusion Matrix pour le meilleur modèle =====
print("\n\n" + "="*80)
print("=== CONFUSION MATRIX (MEILLEUR MODÈLE) ===")
print("="*80)

y_pred_best = results[best_model_name]['y_pred']
cm = confusion_matrix(y_test, y_pred_best)

print(f"\nMatrice de confusion ({best_model_name}) :")
print("\n" + " "*20 + "Prédictions")
print("Réalité       " + "  ".join([f"{le_category.classes_[i]:8}" for i in range(len(le_category.classes_))]))
for i, row in enumerate(cm):
    print(f"{le_category.classes_[i]:8} {row}")

# Visualiser la confusion matrix
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)

# Ajouter les labels
ax.set(xticks=np.arange(cm.shape[1]),
       yticks=np.arange(cm.shape[0]),
       xticklabels=le_category.classes_,
       yticklabels=le_category.classes_,
       ylabel='Réalité',
       xlabel='Prédictions')

# Ajouter les valeurs dans les cellules
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(j, i, format(cm[i, j], 'd'),
                ha="center", va="center",
                color="white" if cm[i, j] > cm.max() / 2 else "black")

fig.colorbar(im, ax=ax)
plt.title(f'Confusion Matrix - {best_model_name} (MOIS + JOUR)')
plt.tight_layout()
plt.savefig('data/processed/confusion_matrix_v3_mois_jour.png', dpi=100, bbox_inches='tight')
print("\n✓ Confusion matrix sauvegardée : confusion_matrix_v3_mois_jour.png")
plt.show()

print("\n" + "="*80)
print("=== ENTRAÎNEMENT TERMINÉ ===")
print("="*80)