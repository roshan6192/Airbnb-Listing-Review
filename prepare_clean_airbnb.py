import pandas as pd

# Load original listings CSV
df = pd.read_csv("Airbnb Data/Listings.csv", encoding="latin1", low_memory=False)

# Standardize column names to lowercase
df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

# Optional renaming to unify key columns
rename_map = {
    "latitude": "latitude",
    "longitude": "longitude",
    "neighbourhood_cleansed": "neighbourhood",
    "room_type": "room_type",
    "minimum_nights": "minimum_nights",
    "bedrooms": "bedrooms",
    "accommodates": "accommodates",
    "review_scores_rating": "review_scores_rating",
    "review_scores_cleanliness": "review_scores_cleanliness",
    "price": "price"
}

df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

# Convert price string to float if needed
if df['price'].dtype == 'object':
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)

# Save clean version
df.to_csv("clean_airbnb.csv", index=False)
print("✅ Clean data saved to clean_airbnb.csv")