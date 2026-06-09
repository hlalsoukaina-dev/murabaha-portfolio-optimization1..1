import streamlit as st
import pandas as pd
from scipy.optimize import linprog

st.title("Modèle de Programmation Linéaire (Allocation Optimale)")

# 1. إدخال المعطيات
budget = st.sidebar.number_input("Budget Total (en millions)", value=1000.0)

# هادو هما "معاملات النمو" اللي كيجيبو التوقع (Predictions)
# تقدري تزيديهم كـ Sliders باش كلما تغير التوقع، تغير النتيجة
g1 = st.sidebar.slider("Taux croissance Immobilier (g1)", 0.05, 0.20, 0.08)
g2 = st.sidebar.slider("Taux croissance Automobile (g2)", 0.02, 0.15, 0.05)
g3 = st.sidebar.slider("Taux croissance Équipement (g3)", 0.01, 0.10, 0.03)

# الدالة الهدف (Maximize Profit)
# linprog كيدير minimization، إذن نضربو فـ -1
c = [-g1, -g2, -g3]

# القيود (Constraints)
# x1 + x2 + x3 = budget
A_eq = [[1, 1, 1]]
b_eq = [budget]

# الحل (هنا فين كاين الـ Intelligence)
res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')

if res.success:
    x1, x2, x3 = res.x
    st.write("### Résultat de l'optimisation :")
    df = pd.DataFrame({
        "Secteur": ["Immobilière", "Automobile", "Équipement"],
        "Allocation Optimale": [x1, x2, x3],
        "Taux Croissance": [g1, g2, g3]
    })
    st.table(df)
    
    st.info(f"Le rendement maximal théorique (Z) est de : {round(-res.fun, 2)} millions.")
else:
    st.error("Le modèle n'a pas pu optimiser.")
