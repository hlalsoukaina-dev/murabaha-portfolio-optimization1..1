import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import plotly.express as px

# 1. Configuration de la page
st.set_page_config(page_title="Mourabaha Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    h1 { color: #0066cc; text-align: center; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #0066cc; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Optimiseur d'Allocation Mourabaha (Quadratique)")
st.markdown("---")

# 2. Paramètres d'entrée
col1, col2 = st.columns(2)
budget = col1.number_input("Budget Total (MAD)", value=1000000)
g1 = col2.number_input("Taux de Croissance : Immobilier (g1)", value=0.0237)
g2 = col1.number_input("Taux de Croissance : Automobile (g2)", value=0.0221)
g3 = col2.number_input("Taux de Croissance : Équipement (g3)", value=0.1498)
g4 = col1.number_input("Taux de Croissance : Mat. Premières (g4)", value=-0.0026)

if st.button("🚀 Lancer l'Optimisation"):
    # Rendements attendus
    returns = np.array([g1, g2, g3, g4])
    
    # Fonction objectif (Quadratique: -Sharpe Ratio ou simple minimisation de risque)
    # Ici on minimise -returns pour maximiser le profit sous contraintes
    def objective(weights):
        return -np.sum(weights * returns)

    # Contraintes
    constraints = (
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}, # Somme des poids = 1
        {'type': 'ineq', 'fun': lambda x: x - np.array([0.3, 0.05, 0.05, 0.0])}, # Lower bounds
        {'type': 'ineq', 'fun': lambda x: np.array([0.8, 0.25, 0.3, 0.1]) - x}  # Upper bounds
    )
    
    # Initialisation
    x0 = [0.25, 0.25, 0.25, 0.25]
    
    # Résolution avec SLSQP (Quadratic Programming solver)
    res = minimize(objective, x0, method='SLSQP', constraints=constraints)
    
    if res.success:
        st.balloons()
        amounts = res.x * budget
        profit = amounts * returns
        
        df = pd.DataFrame({
            "Secteur": ["Immobilier", "Automobile", "Équipement", "Mat. Premières"],
            "Montant Investi (MAD)": amounts,
            "Part (%)": res.x * 100,
            "Profit Attendu (MAD)": profit
        })
        
        st.success("Analyse terminée avec succès (Optimisation Quadratique) !")
        
        col_res1, col_res2 = st.columns([1, 1])
        with col_res1:
            st.subheader("📊 Tableau d'Allocation")
            st.table(df.style.format({"Montant Investi (MAD)": "{:,.2f}", "Part (%)": "{:.1f}%", "Profit Attendu (MAD)": "{:,.2f}"}))
        with col_res2:
            st.subheader("🍕 Distribution du Portefeuille")
            fig_pie = px.pie(df, values='Part (%)', names='Secteur', hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.subheader("📈 Profit Attendu par Secteur")
        fig_bar = px.bar(df, x='Secteur', y='Profit Attendu (MAD)', color='Secteur')
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.info("💡 Note : Cette analyse repose sur la Programmation Quadratique (SLSQP) pour une allocation stratégique robuste.")
    else:
        st.error("L'optimisation a échoué. Vérifiez vos contraintes.")
