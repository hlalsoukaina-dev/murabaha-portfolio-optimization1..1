import streamlit as st
import pandas as pd
from scipy.optimize import linprog

st.title("Optimisation Mourabaha (Modèle Bancaire)")

# القيود (الآن أصبحت نسب مئوية مستقلة)
st.sidebar.header("Répartition des risques")
budget = st.sidebar.number_input("Budget Total", value=1000.0)
p1 = st.sidebar.slider("Poids Immobilier (%)", 0.0, 1.0, 0.4)
p2 = st.sidebar.slider("Poids Automobile (%)", 0.0, 1.0, 0.3)
p3 = st.sidebar.slider("Poids Équipement (%)", 0.0, 1.0, 0.3)

# شرط توازن المحفظة: المجموع يجب أن يساوي الميزانية (x1+x2+x3 = budget)
# والنسب المئوية التي حددتها في السلايدرز
results = {
    "Secteur": ["Immobilière", "Automobile", "Équipement"],
    "Allocation": [budget * p1, budget * p2, budget * p3]
}

df = pd.DataFrame(results)

# عرض النتيجة
st.table(df)

import plotly.express as px
fig = px.pie(df, values='Allocation', names='Secteur', title="Répartition du Portefeuille")
st.plotly_chart(fig)
