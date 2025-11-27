"""Data visualization utilities"""
import pandas as pd
import streamlit as st

@st.cache_data
def load_training_data():
    """Load training metadata for visualizations"""
    df = pd.read_csv('notebook/simple_metadata.csv')
    if df.empty:
        return None
    return df

def plot_class_distribution(df):
    """Plot distribution of skin cancer classes"""
    class_counts = df['dx'].value_counts().reset_index()
    class_counts.columns = ['Class', 'Count']

    st.bar_chart(class_counts.set_index('Class'))

    st.write("""
    **Interpretation:** The dataset shows class imbalance, with 'nv' (melanocytic nevi) 
    being the most common, representing benign moles. Rare classes like 'df' 
    (dermatofibroma) have fewer samples, which can affect model performance.
    """)

def plot_age_distribution(df):
    """Plot age distribution of patients using Streamlit"""
    # Remove NaN ages
    ages = df['age'].dropna()

    # Create age bins
    age_bins = pd.cut(ages, bins=range(0, 100, 5))
    age_counts = age_bins.value_counts().sort_index()
    age_counts.index = age_counts.index.astype(str)

    st.bar_chart(age_counts)

    # Show statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mean Age", f"{ages.mean():.1f} years")
    with col2:
        st.metric("Median Age", f"{ages.median():.1f} years")
    with col3:
        st.metric("Age Range", f"{ages.min():.0f}-{ages.max():.0f}")

    st.write("""
    **Interpretation:** Most skin cancer cases occur in older adults (50-70 years), 
    which aligns with medical research showing increased UV exposure over time 
    as a major risk factor.
    """)

def plot_localization_distribution(df):
    """Plot body location distribution using Streamlit"""
    localization_counts = df['localization'].value_counts().head(10).reset_index()
    localization_counts.columns = ['Location', 'Count']

    st.bar_chart(localization_counts.set_index('Location'))

    st.write("""
    **Interpretation:** Back, lower extremities, and trunk are the most common 
    locations for skin lesions. These areas receive the most sun exposure and are 
    often checked during dermatological examinations.
    """)
