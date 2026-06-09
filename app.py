import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import linprog

# 1. إعداد الصفحة
st.set_page_config(page_title="Optimisation Mourabaha", layout="wide")
st.title("📊 Modèle d'Optimisation : Financements Mourabaha")
st.write("Optimisation de l'allocation basée sur les données de Bank Al-Maghrib (2019-2025).")

# 2. القائمة الجانبية لإدخال المعطيات والقيود
st.sidebar.header("Paramètres du Modèle")

# معدلات النمو (تلقائية من حساباتك السابقة)
st.sidebar.subheader("Taux de croissance (g_i)")
g1 = st.sidebar.slider("Croissance Immobilier (g1)", 0.0, 0.1, 0.0237, format="%.4f")
g2 = st.sidebar.slider("Croissance Automobile (g2)", 0.0, 0.1, 0.0221, format="%.4f")
g3 = st.sidebar.slider("Croissance Équipement (g3)", 0.0, 0.2, 0.1498, format="%.4f")
g4 = st.sidebar.slider("Croissance Mat. Premieres (g4)", -0.05, 0.05, -0.0026, format="%.4f")

# القيود (Bounds)
st.sidebar.subheader("Contraintes (Bornes en %)")
b_immo = st.sidebar.slider("Immobilier", 0.0, 1.0, (0.30, 0.80))
b_auto = st.sidebar.slider("Automobile", 0.0, 1.0, (0.05, 0.25))
b_equip = st.sidebar.slider("Équipement", 0.0, 1.0, (0.05, 0.30))
b_mat = st.sidebar.slider("Mat. Premières", 0.0, 1.0, (0.00, 0.10))

# 3. محرك الحل (Optimization Solver)
c = [-g1, -g2, -g3, -g4] # Négatif pour maximisation
A_eq = [[1, 1, 1, 1]]
b_eq = [1]
bounds = [b_immo, b_auto, b_equip, b_mat]

res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

# 4. عرض النتائج
if res.success:
    results_df = pd.DataFrame({
        "Secteur": ["Immobilier", "Automobile", "Équipement", "Mat. Premières"],
        "Allocation Optimale (%)": [f"{x*100:.2f}%" for x in res.x],
        "Valeur": res.x
    })
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Répartition optimale :")
        st.table(results_df[["Secteur", "Allocation Optimale (%)"]])
    
    with col2:
        import plotly.express as px
        fig = px.pie(results_df, values='Valeur', names='Secteur', title="Visualisation de l'allocation")
        st.plotly_chart(fig)
        
    st.metric("Performance globale (Croissance Z)", f"{-res.fun*100:.2f}%")
else:
    st.error("Le modèle n'a pas trouvé de solution. Vérifiez vos contraintes.")

st.info("Ce modèle démontre l'impact des contraintes du marché sur la performance du portefeuille.")
