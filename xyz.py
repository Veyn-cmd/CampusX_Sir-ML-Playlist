import plotly.express as px
feature = "petal length"

fig = px.line(
    df,
    y=feature,
    x=df.index,
    color='target_name',
    markers=True,
    title=f"{feature.capitalize()} over samples"
)
st.plotly_chart(fig, use_container_width=True)


import plotly.express as px

# Use valid column name
feature = "petal length (cm)"

# Add correct column for color
df['target_name'] = df['species']  # Ensures column exists

fig = px.line(
    df,
    y=feature,
    x=df.index,
    color='target_name',
    markers=True,
    title=f"{feature} over Samples"
)
st.plotly_chart(fig, use_container_width=True)
