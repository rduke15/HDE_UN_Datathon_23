
"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    st.sidebar.markdown(
        "Click the pages above to explore"
    )
    st.sidebar.image('rising_logo.png')
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Read in data for model predictions
    model_predictions = pd.read_csv("./model_outputs/all_counties_predictions.csv")
    model_predictions = model_predictions.rename(columns={'county': 'County', 'prediction':'Model GDP per capita: prediction',
                                                          'true_value': 'True GDP per capita value'})

    # Read in shape files - counties
    level1_boundary = geopandas.read_file("./Datasets/Shape_files/ken_adm_iebc_20191031_shp/ken_admbnda_adm1_iebc_20191031.shp")
    level1_boundary = level1_boundary.rename(columns={'ADM1_EN': 'County'})
    level1_boundary['County'] = level1_boundary['County'].str.lower()
    level1_boundary = level1_boundary.merge(model_predictions, on='County', how='left')

    # Read in shape files - human aspects
    roads = geopandas.read_file("./Datasets/Shape_files/ke_major-roads/ke_major-roads.shp")
    towns = geopandas.read_file("./Datasets/Shape_files/ke_major-towns/ke_major-towns.shp")
    world = geopandas.read_file('./Datasets/Shape_files/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
    kenya = world[world.ADMIN=='Kenya']

    # Create landing page

    st.title("Exploring Kenya's GDP by county")
    st.write("Click on the map counties to explore")

    map_view = st.radio(
        "Choose the map view",
        ["Model output",  "Human features"],horizontal=True,
        captions = ["Model results", "Roads and towns"])

    if map_view == 'Model output': 
        m=level1_boundary[
            ['County', 'ADM1_PCODE','geometry', 'True GDP per capita value',
             'Model GDP per capita: prediction', 'training_example']].explore(column='Model GDP per capita: prediction')
        st_folium(m, width=725)
    elif map_view == 'Human features':
        m = level1_boundary.boundary.explore(color = 'black')
        m = towns.explore(m=m)
        m = roads.explore(m=m, color='red')
        st_folium(m, width=725)

    st.header("Model feature Importance")
    st.write("Summary of feature importance for all counties of Kenya")
    with open(f"./model_outputs/feature_importance.html", 'r', encoding='utf-8') as HtmlFile:
        source_code = HtmlFile.read() 
        components.html(source_code,height = 500,width=1250)


    st.image(['./Data_app/UKRI_STFC_HARTREE_CENTRE_RGB.png','./Data_app/UN_Datathon_logo_with_text.png'], width=150)
