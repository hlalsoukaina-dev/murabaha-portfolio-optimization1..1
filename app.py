import streamlit as st
import pandas as pd
from scipy.optimize import linprog

# --- LOGIQUE MATHÉMATIQUE (Le cœur du sujet) ---
def resoudre_optimisation(g_vals, bounds):
    # الدالة الهدف: max Z = g1*x1 + g2*x2 + g3*x3 + g4*x4
    c = [-g for g in g_vals] 
    A_eq = [[1, 1, 1, 1]] # مجموع النسب = 1 (100%)
    b_eq = [1]
    # الحل باستخدام خوارزمية HiGHS (Linear Programming)
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    return res

# --- INTERFACE (Le tableau de bord) ---
st.title("Moteur d'Optimisation Financière")

# إدخال المعطيات
g_vals = [0.0237, 0.0221, 0.1498, -0.0026] # هادو هما معاملاتك اللي حسبتيهم
# القيود
bounds = [(0.30, 0.80), (0.05, 0.25), (0.05, 0.30), (0.00, 0.10)]

res = resoudre_optimisation(g_vals, bounds)

# --- كشف "السر" الرياضي ---
if res.success:
    st.write("### Analyse du résultat mathématique :")
    # هنا كنشرحوا منطق الحل (Pourquoi cette allocation ?)
    x = res.x
    st.write(f"1. Le modèle a maximisé Z en atteignant une croissance de **{-res.fun*100:.2f}%**.")
    st.write(f"2. **Logique de contrainte :** Pour le secteur Équipement (x3), le modèle a choisi la limite supérieure (**{bounds[2][1]*100}%**) car c'est lui qui offre le meilleur rendement ({g_vals[2]*100:.2f}%).")
    st.write("3. **Logique de diversification :** Les autres secteurs sont ajustés pour respecter les limites (bounds) tout en complétant le budget total à 100%.")
    
    st.table(pd.DataFrame({"Secteur": ["Immo", "Auto", "Équipement", "Mat. Prem"], "Allocation": x}))
