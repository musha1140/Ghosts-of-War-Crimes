import streamlit as st

def header(title, subtitle):
    st.markdown(f"<h1 style='color:#2c3e50;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#7f8c8d;'>{subtitle}</p>", unsafe_allow_html=True)
