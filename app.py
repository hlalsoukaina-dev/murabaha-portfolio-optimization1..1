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
        
        # Calcul des rendements attendus par secteur
        rates = [g1, g2, g3, g4]
        amounts = [x * budget for x in res.x]
        returns = [a * r for a, r in zip(amounts, rates)]
        
        # Préparation des résultats
        df = pd.DataFrame({
            "Secteur": ["Immobilier", "Automobile", "Équipement", "Mat. Premières"],
            "Montant Investi (MAD)": amounts,
            "Part (%)": [x * 100 for x in res.x],
            "Profit Attendu (MAD)": returns
        })
        
        st.success("Analyse terminée avec succès !")
        
        # --- Affichage des Tableaux و المبيانات ---
        
        # الصف الأول: الجدول و الدائرة
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.subheader("📊 Tableau d'Allocation")
            st.table(df.style.format({
                "Montant Investi (MAD)": "{:,.2f}", 
                "Part (%)": "{:.1f}%",
                "Profit Attendu (MAD)": "{:,.2f}"
            }))
            
        with col_res2:
            st.subheader("🍕 Distribution du Portefeuille")
            fig_pie = px.pie(df, values='Part (%)', names='Secteur', hole=0.3, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.markdown("---")
        
        # الصف الثاني: مبيان الأرباح المتوقعة
        st.subheader("📈 Profit Attendu par Secteur (Analyse de Performance)")
        fig_bar = px.bar(df, x='Secteur', y='Profit Attendu (MAD)', 
                         text_auto='.2s', title="Comparaison des Rendements par Secteur",
                         color='Secteur', color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Indice de risque
        risque = "Faible" if res.x[0] > 0.5 else "Élevé"
        st.metric("🛡️ Indice de Risque", risque)
        
        st.info("💡 Note : Cette analyse combine l'optimisation linéaire et la visualisation de performance.")
    else:
        st.error("L'optimisation a échoué. Vérifiez vos contraintes.")
