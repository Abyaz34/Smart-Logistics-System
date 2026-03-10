import streamlit as st
import pandas as pd
import altair as alt
import time
import os

st.set_page_config(layout="wide", page_title="Dobot Dashboard")
st.title("Smart Logistics Dashboard")

script_dir = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(script_dir, 'log.csv')

if not os.path.exists(CSV_FILE):
    st.warning(f"Waiting for CSV file... (Looked in: {script_dir})")
    time.sleep(2)
    st.rerun()

try:
    df = pd.read_csv(CSV_FILE)
except pd.errors.EmptyDataError:
    st.warning("File created, but empty. Waiting for data...")
    time.sleep(2)
    st.rerun()
except Exception as e:
    st.error(f"Error reading CSV: {e}")
    st.stop()

if df.empty:
    st.info("Dataframe is empty. Waiting for blocks...")
else:
    metrics_container = st.container()
    charts_container = st.container()
    
    with metrics_container:
        total = len(df)
        last_cat = df.iloc[-1]['Category']
        last_rel = df.iloc[-1]['Reliability']

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sorted", total)
        col2.metric("Last Category", str(last_cat))
        col3.metric("Reliability", f"{float(last_rel)*100:.1f}%")

    with charts_container:
        st.subheader("Frequency")
        st.bar_chart(df['Category'].value_counts())

    st.subheader("Raw Data")
    styled_df = df.sort_index(ascending=False).style.set_properties(**{
        'text-align': 'center'
    })
    st.dataframe(styled_df, width="stretch")

time.sleep(2)
st.rerun()