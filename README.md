# Impf-Counter

This repository contains the code for a COVID-19 vaccine counter dashboard

## Running with Docker

```
docker build -t impfcounter:latest .

docker container run -p 8501:8501 --name impfcounter impfcounter:latest
```

## Running with Streamlit

```
pip install streamlit

streamlit run visualisation.py
```

Important: You need to run everything in an geopandas environment. See this tutorial https://medium.com/@sourav_raj/ultimate-easiest-way-to-install-geopandas-on-windows-add-to-jupyter-notebook-which-will-a4b11223f4f2

