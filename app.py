import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعداد الصفحة
st.set_page_config(page_title="Optimisation Portefeuille", layout="wide")
st.title("Optimisation du Portefeuille Financier")

# 2. تحميل الداتا
# تأكدي أن ملف data.xlsx موجود فـ نفس الفولدر فـ GitHub
try:
    df = pd.read_excel('data.xlsx')
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier : {e}")
    st.stop()

# 3. القائمة الجانبية للقيود (Sliders)
st.sidebar.header("Paramètres des contraintes")
min_immob = st.sidebar.slider("Limite Min Immobilier", 0.0, 1.0, 0.27)
min_auto = st.sidebar.slider("Limite Min Automobile", 0.0, 1.0, 0.25)
min_equip = st.sidebar.slider("Limite Min Equipement", 0.0, 1.0, 0.10)
min_mat = st.sidebar.slider("Limite Min Matières", 0.0, 1.0, 0.05)

# 4. عرض البيانات
st.subheader("Aperçu des données")
st.dataframe(df.head())

# 5. حساب الـ Rendement بشكل تفاعلي
# هنا كنربطوا النتيجة بالقيم اللي اختاريتي فـ الـ Sliders
rendement = (min_immob * 12) + (min_auto * 8) + (min_equip * 6) + (min_mat * 4)

st.success(f"### Rendement Attendu : {rendement:.2f}%")

# 6. غراف توزيع الاستثمارات
st.subheader("Distribution du Portefeuille")
data_to_plot = pd.DataFrame({
    'Secteur': ['Immobilier', 'Automobile', 'Equipement', 'Matières'],
    'Valeur': [min_immob, min_auto, min_equip, min_mat]
})

fig = px.pie(data_to_plot, values='Valeur', names='Secteur', hole=0.3)
st.plotly_chart(fig)
