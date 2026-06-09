import streamlit as st
import pandas as pd
from scipy.optimize import linprog

st.title("Optimisation Mourabaha (Modèle Dynamique)")

# 1. إدخال جميع القيود عبر Sliders (هنا كنزيدو المرونة)
st.sidebar.header("Paramètres des contraintes")
budget = st.sidebar.number_input("Budget Total (en millions)", value=1000.0)
min_immo = st.sidebar.slider("Part min Immobilière (x1) %", 0.0, 1.0, 0.5)
max_auto = st.sidebar.slider("Part max Automobile (x2) %", 0.0, 1.0, 0.3)

# 2. معاملات النمو (g1, g2, g3) - تقدري تغيريهم حسب الداتا ديالك
g = [-0.08, -0.05, -0.03] 

# 3. بناء مصفوفة القيود ديناميكياً
# x1 + x2 + x3 <= budget
# x1 >= min_immo * budget  => -x1 <= -min_immo * budget
# x2 <= max_auto * budget
A_ub = [
    [1, 1, 1],       # Budget
    [-1, 0, 0],      # Immo min
    [0, 1, 0]        # Auto max
]
b_ub = [budget, -min_immo * budget, max_auto * budget]

# 4. الحل
res = linprog(g, A_ub=A_ub, b_ub=b_ub, bounds=(0, None), method='highs')

if res.success:
    x1, x2, x3 = res.x
    results_df = pd.DataFrame({
        "Type": ["Immobilière", "Automobile", "Équipement"],
        "Valeur Optimale": [x1, x2, x3]
    })
    
    st.table(results_df)
    
    import plotly.express as px
    fig = px.pie(results_df, values='Valeur Optimale', names='Type', title="Répartition Optimale")
    st.plotly_chart(fig)
else:
    st.error("Impossible de trouver une solution avec ces contraintes. Essaie de modifier les curseurs.")
