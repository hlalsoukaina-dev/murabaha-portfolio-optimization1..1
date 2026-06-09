import streamlit as st
import pandas as pd
from scipy.optimize import linprog

# 1. تصميم الواجهة (Layout)
st.set_page_config(page_title="Mourabaha Optimizer", layout="centered")
st.title("🏦 Mourabaha Allocation Optimizer")
st.markdown("---")

# 2. إدخال المعطيات في خانات منظمة (Form)
with st.form("input_form"):
    st.subheader("Entrez vos paramètres")
    budget = st.number_input("Budget Total (MAD)", value=1000000)
    
    col1, col2 = st.columns(2)
    g1 = col1.number_input("Taux Croissance Immo (g1)", value=0.0237, format="%.4f")
    g2 = col2.number_input("Taux Croissance Auto (g2)", value=0.0221, format="%.4f")
    g3 = col1.number_input("Taux Croissance Equip (g3)", value=0.1498, format="%.4f")
    g4 = col2.number_input("Taux Croissance Mat (g4)", value=-0.0026, format="%.4f")
    
    submitted = st.form_submit_button("Calculer l'Allocation Optimale")

# 3. محرك الحساب (الـ Logic)
if submitted:
    c = [-g1, -g2, -g3, -g4]
    bounds = [(0.3, 0.8), (0.05, 0.25), (0.05, 0.3), (0.0, 0.1)]
    res = linprog(c, A_eq=[[1, 1, 1, 1]], b_eq=[1], bounds=bounds, method='highs')
    
    if res.success:
        st.success("Calcul effectué avec succès !")
        results = pd.DataFrame({
            "Secteur": ["Immo", "Auto", "Equipement", "Mat. Premieres"],
            "Montant (MAD)": [x * budget for x in res.x],
            "Part (%)": [f"{x*100:.1f}%" for x in res.x]
        })
        st.table(results)
    else:
        st.error("Erreur dans le calcul !")
