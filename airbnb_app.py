import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import folium_static
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Airbnb Analysis", layout="wide")
st.title("🏘 Airbnb Analysis Dashboard")

# Load model and dataset
@st.cache_resource
def load_model():
    return joblib.load("price_model.pkl")

@st.cache_data
def load_data():
    return pd.read_csv("clean_airbnb.csv")

model = load_model()
df = load_data()

# Create tabs
tab1, tab2, tab3 = st.tabs(["💰 Price Prediction", "🗺 Map", "📊 Clustering"])

# --- PRICE PREDICTION ---
with tab1:
    st.header("💰 Predict Listing Price")

    neighbourhoods = df['neighbourhood'].dropna().unique().tolist()
    room_types = df['room_type'].dropna().unique().tolist()

    neighbourhood = st.selectbox("Neighbourhood", neighbourhoods)
    room_type = st.selectbox("Room Type", room_types)
    minimum_nights = st.number_input("Minimum Nights", min_value=1, value=2)
    bedrooms = st.number_input("Bedrooms", min_value=0, value=1)
    accommodates = st.number_input("Accommodates", min_value=1, value=2)
    review_scores_rating = st.slider("Review Score Rating", 0.0, 100.0, 80.0)
    review_scores_cleanliness = st.slider("Review Score Cleanliness", 0.0, 10.0, 8.0)

    if st.button("Predict Price"):
        input_df = pd.DataFrame([{
            "neighbourhood": neighbourhood,
            "room_type": room_type,
            "minimum_nights": minimum_nights,
            "bedrooms": bedrooms,
            "accommodates": accommodates,
            "review_scores_rating": review_scores_rating,
            "review_scores_cleanliness": review_scores_cleanliness
        }])
        price = model.predict(input_df)[0]
        st.success(f"Estimated Price: ${price:,.2f} per night")

# --- MAP TAB ---
with tab2:
    st.header("🗺 Map of Listings")
    df_map = df.dropna(subset=["latitude", "longitude", "price", "room_type"])
    m = folium.Map(location=[df_map.latitude.mean(), df_map.longitude.mean()], zoom_start=12)

    for _, row in df_map.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"${row['price']} - {row['room_type']}"
        ).add_to(m)

    folium_static(m)

# --- CLUSTERING TAB ---
with tab3:
    st.header("📊 Clustering of Listings by Location")

    coords = df[['latitude', 'longitude']].dropna()
    k = st.slider("Number of Clusters", 2, 10, 5)

    kmeans = KMeans(n_clusters=k, random_state=42)
    df['cluster'] = kmeans.fit_predict(coords)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='longitude', y='latitude', hue='cluster', palette='tab10', ax=ax)
    ax.set_title("Listing Clusters")
    st.pyplot(fig)
