import streamlit as st
import functions

st.set_page_config(
    page_title="CARGATRON",
    page_icon="random",
    layout="wide"
)

with st.sidebar:
    menu_selectbox = st.selectbox("What do you want to see?", ["<< Home >>", "<< Data >>"])

if menu_selectbox == "<< Home >>":
    functions.home()
else:
    functions.data()








