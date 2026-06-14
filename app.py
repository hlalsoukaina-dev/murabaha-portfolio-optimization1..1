import streamlit as st
import pandas as pd
from scipy.optimize import linprog
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

st.title("🏦 Optimiseur d'Allocation Mourabaha")
st.markdown("---")

# 2. Paramètres d'entrée
col1, col2 = st.columns(2)
budget = col1.number_input("Budget Total (MAD)", value=1000000)
g1 = col2.number_input("Taux de Croissance : Immobilier (g1)", value=0.0237)
g2 = col1.number_input("Taux de Croissance : Automobile (g2)", value=0.0221)
g3 = col2.number_input("Taux de Croissance : Équipement (g3)", value=0.1498)
g4 = col1.number_input("Taux de Croissance : Mat. Premières (g4)", value=-0.0026)

if st.button("🚀 Lancer l'Optimisation"):
    # Objectif: Maximiser les rendements
    c = [-g1, -g2, -g3, -g4]
    
    # Contraintes: Limites par secteur
    bounds = [(0.3, 0.8), (0.05, 0.25), (0.05, 0.3), (0.0, 0.1)]
    
    # Résolution
    res = linprog(c, A_eq=[[1, 1, 1, 1]], b_eq=[1], bounds=bounds, method='highs')
    
    if res.success:
        st.balloons()
        
        # Préparation des résultats
        df = pd.DataFrame({
            "Secteur": ["Immobilier", "Automobile", "Équipement", "Mat. Premières"],
            "Montant (MAD)": [x * budget for x in res.x],
            "Part (%)": [x * 100 for x in res.x]
        })
        
        st.success("Analyse terminée avec succès !")
        
        # Affichage
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.subheader("Tableau d'Allocation Optimisée")
            st.table(df.style.format({"Montant (MAD)": "{:,.2f}", "Part (%)": "{:.1f}%"}))
            
        with col_res2:
            st.subheader("Visualisation")
            fig = px.pie(df, values='Part (%)', names='Secteur', hole=0.3)
            st.plotly_chart(fig)
        
        # Indice de risque
        risque = "Faible" if res.x[0] > 0.5 else "Élevé"
        st.metric("Indice de Risque de Diversification", risque)
        
        st.info("💡 Note : Les résultats sont générés via la programmation quadratique sous contraintes.")
    else:
        st.error("L'optimisation a échoué. Vérifiez vos contraintes.")
