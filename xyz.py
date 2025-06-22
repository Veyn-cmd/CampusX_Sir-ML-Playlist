# 📦 Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.datasets import load_iris

# 🔧 Configure the Streamlit app
st.set_page_config(
    page_title="🌼 Iris Dataset Explorer",
    page_icon="🌼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 📥 Load the Iris dataset
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
df['species'] = df['target'].apply(lambda x: iris.target_names[x])
df['target_name'] = df['species']  # For Plotly coloring

# 📌 App Title
st.title("🌸 Iris Dataset Explorer")
st.write("Explore one of the most famous datasets in machine learning with visualizations and interactivity.")

# 📄 Show Raw Data
if st.checkbox("🔍 Show Raw Data"):
    st.dataframe(df)

# 🔘 Select a species to filter
species = st.selectbox("🌱 Select a species", iris.target_names)
filtered_df = df[df['species'] == species]
st.write(f"📌 Showing data for: **{species}**")

# 📊 Summary Stats
st.subheader("📊 Summary Statistics")
st.write(filtered_df.describe())

# 📈 Feature Comparison Plot (Seaborn Scatter)
st.subheader("📉 Feature Comparison: Scatter Plot")

x_feature = st.selectbox("📌 X-axis Feature", iris.feature_names)
y_feature = st.selectbox("📌 Y-axis Feature", iris.feature_names, index=1)

fig1, ax1 = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x=x_feature,
    y=y_feature,
    hue="species",
    palette="viridis",
    ax=ax1
)
ax1.set_title(f"{x_feature} vs {y_feature}")
st.pyplot(fig1)

# 📊 Pairplot (Full dataset)
st.subheader("📊 Pairplot (Full Dataset)")
fig_pair = sns.pairplot(df, hue="species", corner=True, palette="cool")
st.pyplot(fig_pair)

# 📈 Plotly Line Chart of a Feature
st.subheader("📈 Plotly Line Plot: Feature Over Samples")

feature_plot = st.selectbox("Choose a feature to visualize", iris.feature_names, index=2)

fig2 = px.line(
    df,
    y=feature_plot,
    x=df.index,
    color='target_name',
    markers=True,
    title=f"{feature_plot} Over Samples"
)
st.plotly_chart(fig2, use_container_width=True)
