import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
from collections import Counter

warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(page_title="Aircraft Crash Analytics", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("planecrashinfo_20181121001952.csv")
    df = df.replace('?', np.nan)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['Date'] = df['date']
    return df

df = load_data()

st.title("✈️ Aircraft Crash Analysis Dashboard")

# Sidebar Filters
with st.sidebar:
    st.header("Controls")
    min_year = int(df['date'].dt.year.min())
    max_year = int(df['date'].dt.year.max())
    year_range = st.slider("Year Range", min_year, max_year, (min_year, max_year))
    show_advanced = st.checkbox("Show Advanced Sections")

# Preprocessing
df['Year'] = df['date'].dt.year
df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
df['weekday_name'] = df['date'].dt.day_name()
df['day_of_month'] = df['date'].dt.day
df['month'] = df['date'].dt.month_name()
df['quarter'] = df['date'].dt.quarter

# Time cleaning
def clean_time(t):
    if pd.isna(t):
        return np.nan
    t = str(t).strip().lower().replace('c ', '')
    if ':' in t:
        try:
            return int(t.split(':')[0])
        except:
            return np.nan
    return np.nan

df['hour'] = df['time'].apply(clean_time)
df['am_pm'] = df['hour'].apply(lambda x: 'AM' if pd.notna(x) and x < 12 else 'PM')
df['day_night'] = df['hour'].apply(lambda x: 'Day (6AM–6PM)' if pd.notna(x) and 6 <= x < 18 else 'Night (6PM–6AM)')

# SECTION: Yearly Crash Trend
with st.container():
    st.subheader("📉 Yearly Aircraft Crashes")
    crashes_per_year = df.groupby('Year').size().reset_index(name='Crashes')

    # Simulated flight growth for crash rate
    flight_growth = {
        year: int(1_000_000 * (1.05 ** (year - min_year))) for year in range(min_year, max_year + 1)
    }
    flights_df = pd.DataFrame(list(flight_growth.items()), columns=['Year', 'Total_Flights'])
    crash_rate_df = pd.merge(crashes_per_year, flights_df, on='Year', how='left')
    crash_rate_df['Crash_Rate_Percentage'] = (crash_rate_df['Crashes'] / crash_rate_df['Total_Flights']) * 100

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=crash_rate_df, x='Year', y='Crashes', marker='o', color='crimson', ax=ax)
    ax.set_title("Number of Plane Crashes per Year")
    st.pyplot(fig)

    fig2, ax2 = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=crash_rate_df, x='Year', y='Crash_Rate_Percentage', marker='o', color='teal', ax=ax2)
    ax2.set_title("Crash Rate (%) of Total Estimated Flights")
    st.pyplot(fig2)

# SECTION: Weekly/Monthly Trends
with st.container():
    st.subheader("📅 Temporal Patterns of Crashes")
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(data=df, x='weekday_name', order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], palette='Dark2', ax=ax)
        ax.set_title("Crashes by Weekday")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(data=df, x='month', order=pd.date_range('2024-01-01', periods=12, freq='M').strftime('%B'), palette='Dark2', ax=ax)
        ax.set_title("Crashes by Month")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

# SECTION: Time of Day Analysis
with st.container():
    st.subheader("🕒 Crashes by Time of Day")

    fig, axes = plt.subplots(1, 3, figsize=(20, 5))
    if not df['am_pm'].dropna().empty:
        df_am_pm = df.dropna(subset=['am_pm'])
        axes[0].pie(df_am_pm['am_pm'].value_counts(), labels=df_am_pm['am_pm'].unique(),
                    autopct='%1.1f%%', colors=sns.color_palette('dark'))
        axes[0].add_artist(plt.Circle((0, 0), 0.7, color='white'))
        axes[0].set_title("AM/PM")

    if not df['day_night'].dropna().empty:
        axes[1].pie(df['day_night'].value_counts(), labels=df['day_night'].unique(),
                    autopct='%1.1f%%', colors=sns.color_palette('dark'))
        axes[1].add_artist(plt.Circle((0, 0), 0.7, color='white'))
        axes[1].set_title("Day vs Night")

    sns.countplot(data=df, x='hour', ax=axes[2], palette='Dark2')
    axes[2].set_title("Crashes by Hour")
    axes[2].set_xlabel("Hour (0-23)")
    st.pyplot(fig)

# SECTION: Aircraft Models
with st.container():
    st.subheader("🛩️ Most Common Aircraft in Crashes")

    top_models = df['ac_type'].dropna().value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(x=top_models.values, y=top_models.index, palette='Dark2', ax=ax)
    ax.set_title("Top 10 Aircraft Models by Crashes")
    st.pyplot(fig)

# SECTION: Heatmap by Decade and Model
if show_advanced:
    st.subheader("📊 Crashes per Aircraft Model by Decade")

    df['decade'] = (df['date'].dt.year // 10) * 10
    df_clean = df.dropna(subset=['ac_type', 'decade'])
    filtered = df_clean[df_clean['ac_type'].isin(top_models.index)]

    pivot = filtered.pivot_table(index='decade', columns='ac_type', aggfunc='size', fill_value=0)
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(pivot, annot=True, fmt='d', cmap='Purples', ax=ax)
    st.pyplot(fig)

# SECTION: Geographic Map
with st.container():
    st.subheader("🌍 Global Distribution of Crashes")

    df['location'] = df['location'].fillna('')
    df['country'] = df['location'].apply(lambda loc: loc.split(',')[-1].strip())
    country_crash_counts = df['country'].value_counts().reset_index()
    country_crash_counts.columns = ['country', 'crashes']
    country_crash_counts = country_crash_counts[country_crash_counts['country'].str.len() > 1]

    fig = px.choropleth(
        country_crash_counts,
        locations='country',
        locationmode='country names',
        color='crashes',
        hover_name='country',
        color_continuous_scale='Reds'
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

# SECTION: Waterbody Analysis
if show_advanced:
    st.subheader("🌊 Crashes Mentioning Waterbodies")

    known_waterbodies = [
        "atlantic ocean", "pacific ocean", "indian ocean", "arctic ocean",
        "bering sea", "caribbean sea", "mediterranean sea", "black sea",
        "north sea", "baltic sea", "caspian sea", "hudson bay", "lake michigan",
        "lake superior", "lake huron", "lake erie", "lake ontario", "english channel"
    ]

    matched_bodies = []
    for loc in df['location'].dropna().str.lower():
        for wb in known_waterbodies:
            if wb in loc:
                matched_bodies.append(wb)

    wb_df = pd.DataFrame(Counter(matched_bodies).most_common(10), columns=['Waterbody', 'Crash_Count'])
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=wb_df, x='Crash_Count', y='Waterbody', palette='Blues_d', ax=ax)
    st.pyplot(fig)

