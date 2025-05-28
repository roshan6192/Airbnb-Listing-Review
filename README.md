# 🏘 Airbnb Streamlit Dashboard (Dockerized)

## 📂 Contents
- `app.py`: Streamlit app for prediction, mapping, and clustering
- `prepare_clean_airbnb.py`: Script to clean and prepare `Listings.csv`
- `Dockerfile`: Container definition
- `requirements.txt`: Python dependencies

## 🚀 How to Run

### 1. Prepare the data
```bash
python prepare_clean_airbnb.py
```

Make sure you have `Airbnb Data/Listings.csv` in the correct folder.

### 2. Run Streamlit app locally
```bash
streamlit run app.py
```

### 3. Run with Docker
```bash
docker build -t airbnb-app .
docker run -p 8501:8501 airbnb-app
```

Then open http://localhost:8501

---
> Created by Roshan Thomas