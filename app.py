import streamlit as st
import pandas as pd
import plotly.express as px

# 1. تحميل الداتا
# تأكدي أن الملف سميتو data.xlsx ومحطوط فـ نفس الفولدر
df = pd.read_excel('data.xlsx')

st.title("Optimisation du Portefeuille Financier")

# 2. القائمة الجانبية للقيود
st.sidebar.header("Paramètres des contraintes")
min_immob = st.sidebar.slider("Limite Min Immobilier", 0.0, 1.0, 0.27)
min_auto = st.sidebar.slider("Limite Min Automobile", 0.0, 1.0, 0.25)
min_equip = st.sidebar.slider("Limite Min Equipement", 0.0, 1.0, 0.10)
min_mat = st.sidebar.slider("Limite Min Matières", 0.0, 1.0, 0.05)

# 3. عرض الداتا
st.subheader("Aperçu des données")
st.dataframe(df.head())

# 4. حساب النتيجة (باستعمال iloc باش نتفاداو الـ KeyError)
# كياخد العواميد من 1 لـ 4 (القطاعات)
total_mean = df.iloc[:, 1:5].mean()
rendement = (total_mean.sum() / df['Totale'].mean()) * 100

st.success(f"Rendement Attendu moyen : {rendement:.2f}%")

# 5. غراف توزيع القطاعات
st.subheader("Distribution du Portefeuille")
fig = px.pie(values=total_mean, names=total_mean.index, title="Répartition des investissements")
st.plotly_chart(fig)
