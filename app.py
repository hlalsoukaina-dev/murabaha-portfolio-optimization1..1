import streamlit as st
import pandas as pd
from scipy.optimize import linprog

st.title("Optimisation Mourabaha (Modèle Dynamique)")

st.sidebar.header("Paramètres")

# القيود اللي بغيتيها تكون ديناميكية ومستقلة
budget = st.sidebar.number_input("Budget Total", value=1000.0)
min_immo = st.sidebar.slider("Immobilier Min (x1)", 0.0, 0.8, 0.3)
max_auto = st.sidebar.slider("Automobile Max (x2)", 0.0, 0.8, 0.3)
max_equip = st.sidebar.slider("Équipement Max (x3)", 0.0, 0.8, 0.3)

# معاملات النمو (هادو هما اللي كيعطيو القيمة لـ Max Z)
g1, g2, g3 = 0.08, 0.05, 0.03
c = [-g1, -g2, -g3]

# المصفوفة الديناميكية
# هنا كنزيدو قيود (Boundaries) لكل متغير x1, x2, x3 باش ميبقاش تابع غير للـ budget
A_ub = [[1, 1, 1]] 
b_ub = [budget]

# باش الـ Solver يحترم القيود اللي حددتيهم فـ الـ Sliders
bounds = [
    (min_immo * budget, None),  # x1 min
    (0, max_auto * budget),     # x2 max
    (0, max_equip * budget)     # x3 max
]

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

if res.success:
    x1, x2, x3 = res.x
    # الجدول اللي سوتي عليه: كيبين شحال كل sector خدا من الميزانية بناءً على الـ Logic ديالك
    df = pd.DataFrame({
        "Secteur": ["Immobilière", "Automobile", "Équipement"],
        "Allocation": [x1, x2, x3]
    })
    st.table(df)
    
    import plotly.express as px
    fig = px.pie(df, values='Allocation', names='Secteur')
    st.plotly_chart(fig)
else:
    st.error("Les contraintes sont trop strictes, le modèle ne peut pas trouver de solution.")
