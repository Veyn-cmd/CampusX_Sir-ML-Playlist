import streamlit as st
from sklearn.datasets import load_iris
import pandas as pd

# Load dataset
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
df['species'] = df['target'].apply(lambda x: iris.target_names[x])

# Streamlit App
st.title("🌸 Iris Dataset Explorer")
st.write("Explore one of the most famous datasets in machine learning.")

# Show full data
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Select species
species = st.selectbox("Select a species", iris.target_names)

# Filter data
filtered_df = df[df['species'] == species]
st.write(f"Showing data for: **{species}**")

# Show summary stats
st.write("📊 Summary Statistics")
st.write(filtered_df.describe())

import matplotlib.pyplot as plt
import seaborn as sns

# Visualization Section
st.write("📈 Feature Comparison Plot")

# Let user pick 2 features to compare
x_feature = st.selectbox("X-axis feature", iris.feature_names)
y_feature = st.selectbox("Y-axis feature", iris.feature_names, index=1)

# Plot with seaborn
fig, ax = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x=x_feature,
    y=y_feature,
    hue="species",
    palette="viridis",
    ax=ax
)

ax.set_title(f"{x_feature} vs {y_feature}")
st.pyplot(fig)

if st.checkbox("Show Pairplot"):
    st.write("🔍 Pairplot of all features")
    fig_pair = sns.pairplot(df, hue="species", corner=True, palette="cool")
    st.pyplot(fig_pair)


