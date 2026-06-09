import streamlit as st
import pandas as pd
from scipy.optimize import linprog

# 1. إعداد الصفحة بألوان وتنسيق
st.set_page_config(page_title="Mourabaha Pro", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    h1 { color: #0066cc; text-align: center; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #0066cc; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Mourabaha Allocation Optimizer")
st.markdown("---")

# 2. إدخال المعطيات
col1, col2 = st.columns(2)
budget = col1.number_input("Budget Total (MAD)", value=1000000)
g1 = col2.number_input("Taux Croissance Immo (g1)", value=0.0237)
g2 = col1.number_input("Taux Croissance Auto (g2)", value=0.0221)
g3 = col2.number_input("Taux Croissance Equip (g3)", value=0.1498)
g4 = col1.number_input("Taux Croissance Mat. (g4)", value=-0.0026)

if st.button("🚀 Lancer l'Analyse"):
    c = [-g1, -g2, -g3, -g4]
    bounds = [(0.3, 0.8), (0.05, 0.25), (0.05, 0.3), (0.0, 0.1)]
    res = linprog(c, A_eq=[[1, 1, 1, 1]], b_eq=[1], bounds=bounds, method='highs')
    
    if res.success:
        st.balloons() # اللمسة التفاعلية
        
        # النتائج
        df = pd.DataFrame({
            "Secteur": ["Immo", "Auto", "Equipement", "Mat. Premieres"],
            "Montant (MAD)": [x * budget for x in res.x],
            "Part (%)": [x * 100 for x in res.x]
        })
        
        # عرض احترافي
        st.success("Analyse terminée avec succès !")
        st.table(df.style.format({"Montant (MAD)": "{:,.2f}", "Part (%)": "{:.1f}%"}))
        
        # لمسة إضافية: مؤشر المخاطر (بسيط)
        risk = "Faible" if res.x[0] > 0.5 else "Élevé"
        st.metric("Indice de Diversification", risk)
        
        st.info("💡 Note : Les résultats sont basés sur une optimisation sous contraintes de marché.")
