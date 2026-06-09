import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import linprog

st.title("Optimisation des Financements Mourabaha")
st.write("Modèle de programmation linéaire basé sur les données de Bank Al-Maghrib.")

# 1. إدخال القيود عبر Sliders
st.sidebar.header("Paramètres des contraintes")
budget = st.sidebar.number_input("Budget Total (en millions)", min_value=100, value=1000)
min_immo = st.sidebar.slider("Part minimale Mourabaha Immobilière (x1) %", 0.0, 1.0, 0.6)

# 2. معاملات النمو (g1, g2, g3) - هادو تقدري تبدليهم بأرقام حقيقية من BAM
g = [-0.08, -0.05, -0.03]  # ملاحظة: نضع إشارة سالب لأن linprog يقوم بعملية Minimization

# 3. إعداد مصفوفة القيود
# x1 + x2 + x3 <= budget
# x1 >= min_immo * budget  => -x1 <= -min_immo * budget
A_ub = [[1, 1, 1], [-1, 0, 0]]
b_ub = [budget, -min_immo * budget]

# 4. الحل باستخدام Solver
res = linprog(g, A_ub=A_ub, b_ub=b_ub, bounds=(0, None), method='highs')

if res.success:
    x1, x2, x3 = res.x
    st.success("Optimisation réussie !")
    
    # عرض النتائج
    results_df = pd.DataFrame({
        "Type de Financement": ["Immobilière (x1)", "Automobile (x2)", "Équipement (x3)"],
        "Montant Optimal": [x1, x2, x3]
    })
    
    st.table(results_df)
    
    # غراف النتائج
    import plotly.express as px
    fig = px.pie(results_df, values='Montant Optimal', names='Type de Financement', title="Allocation Optimale")
    st.plotly_chart(fig)
else:
    st.error("Le modèle n'a pas trouvé de solution optimale avec ces contraintes.")
