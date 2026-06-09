import streamlit as st
import pandas as pd
from scipy.optimize import linprog

st.title("Optimisation Mourabaha (Modèle Dynamique)")

st.sidebar.header("Paramètres du Modèle")

# 1. إدخال الميزانية والقيود من طرف المستخدم
budget = st.sidebar.number_input("Budget Total", value=1000.0)
min_immo = st.sidebar.slider("Part minimale Immobilière (x1)", 0.0, 1.0, 0.5)
max_auto = st.sidebar.slider("Part maximale Automobile (x2)", 0.0, 1.0, 0.4)

# 2. إدخال معاملات النمو (هنا فين كيولي الـ Solver ديناميكي)
st.sidebar.subheader("Taux de croissance (g)")
g1 = st.sidebar.slider("Croissance Immo (g1)", 0.0, 0.2, 0.08)
g2 = st.sidebar.slider("Croissance Auto (g2)", 0.0, 0.2, 0.05)
g3 = st.sidebar.slider("Croissance Équipement (g3)", 0.0, 0.2, 0.03)

# المعادلة: Max Z = g1*x1 + g2*x2 + g3*x3
# الـ Solver كيخدم بـ Minimization، لذا نضربوا في -1
c = [-g1, -g2, -g3]

# القيود (Constraints)
A_ub = [
    [1, 1, 1],       # x1 + x2 + x3 <= budget
    [-1, 0, 0],      # x1 >= min_immo * budget  => -x1 <= -min_immo * budget
    [0, 1, 0]        # x2 <= max_auto * budget
]
b_ub = [budget, -min_immo * budget, max_auto * budget]

# الحل
res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=(0, None), method='highs')

if res.success:
    x1, x2, x3 = res.x
    df = pd.DataFrame({
        "Secteur": ["Immobilière (x1)", "Automobile (x2)", "Équipement (x3)"],
        "Allocation Optimale": [x1, x2, x3]
    })
    st.table(df) # هذا هو الجدول اللي كيورينا التوزيع النهائي
    
    import plotly.express as px
    fig = px.pie(df, values='Allocation Optimale', names='Secteur')
    st.plotly_chart(fig)
else:
    st.error("Aucune solution trouvée. Ajustez les curseurs.")
