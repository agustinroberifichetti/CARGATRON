import streamlit as st
import pandas as pd


def home():

    st.title("Welcome to CARGATRON")
    st.subheader("Find your nearest point of charge!")
    st.image("Ejercicio/2019030219064292568.jpg")
    with st.expander("Click here to learn more"):
        st.write("""Look for every charging point for you car in Madrid with CARGATRON mapping tool! Peluca uses it, why wouldn't you?""")

    uploaded_file = st.file_uploader("Upload your .csv type file:", type="csv")

    @st.cache(suppress_st_warning=True)
    def balloons():
        st.balloons()

    if uploaded_file != None:
        with st.echo():
            st.write("Your uploaded data:")
            st.dataframe(pd.read_csv(uploaded_file, sep=";"))
        balloons()

    else:
        st.write("Default data:")
        st.dataframe(pd.read_csv("Ejercicio/data/red_recarga_acceso_publico_2021.csv", sep=";"))


def data():

    col1, col2 = st.columns([3, 2])

    data_frame = pd.DataFrame(pd.read_csv("Ejercicio/data/red_recarga_acceso_publico_2021.csv", sep=";"))
    data_frame.columns = list(data_frame.columns)[:7] + ["longitude", "latitude"]
    cargadores_por_distrito = data_frame.groupby("DISTRITO").sum("N° CARGADORES").iloc[:, :1]
    cargadores_por_operador = data_frame.groupby("OPERADOR").sum("N° CARGADORES").iloc[:, :1]

    with st.sidebar:
        operador_checkbox = st.checkbox("> Activate filter", key="op")
        operador_selectbox = st.selectbox("Choose an Operator:", data_frame["OPERADOR"].unique())

        district_checkbox = st.checkbox("> Activate filter", key="dis")
        distrito_selectbox = st.selectbox("Choose a District:", data_frame["DISTRITO"].unique())

    zoom = 11
    if operador_checkbox and district_checkbox:
        map_data_frame = data_frame[(data_frame["OPERADOR"] == operador_selectbox) & (data_frame["DISTRITO"] == distrito_selectbox)]
        zoom = 13
    elif operador_checkbox:
        map_data_frame = data_frame[data_frame["OPERADOR"] == operador_selectbox]
    elif district_checkbox:
        map_data_frame = data_frame[data_frame["DISTRITO"] == distrito_selectbox]
        zoom = 13
    else:
        map_data_frame = data_frame

    with col1:
        if map_data_frame["longitude"].count() == 0:
            st.warning("The are no matches for the selected combination of filters", icon="⚠️")
            st.stop()
        else:
            st.write("Distribution of charging points:")
            st.map(map_data_frame, zoom=zoom)

    with col2:
        if not district_checkbox:
            st.write("Charging points per District:")
            st.bar_chart(cargadores_por_distrito, width=700, height=500, use_container_width=False)

        if not operador_checkbox:
            st.write("Charging points per Operator:")
            st.bar_chart(cargadores_por_operador, width=700, height=500, use_container_width=False)



