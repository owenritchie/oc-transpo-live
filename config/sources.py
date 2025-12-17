import streamlit as st
import psycopg2
import pandas as pd



@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets['postgres'])

@st.cache_data(ttl = 600)
def get_active_transit_data():
    conn = init_connection()
    query = "SELECT * FROM public.fct_active_vehicles"
    return pd.read_sql_query(query, conn)

@st.cache_data(ttl = 600)
def get_historical_transit_data():
    conn = init_connection()
    query = "SELECT * FROM public.oc_historical_snapshots"
    return pd.read_sql_query(query, conn)