
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
st.set_option('deprecation.showPyplotGlobalUse', False)
level1_boundary = geopandas.read_file("./Datasets/Shape files/ken_adm_iebc_20191031_shp/ken_admbnda_adm1_iebc_20191031.shp")
roads = geopandas.read_file("./Datasets/Shape files/ke_major-roads/ke_major-roads.shp")
towns = geopandas.read_file("./Datasets/Shape files/ke_major-towns/ke_major-towns.shp")
world = geopandas.read_file('./Datasets/Shape files/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
kenya = world[world.ADMIN=='Kenya']

st.write("This is our app")
map_view = st.radio(
    "Choose the map view",
    ["Model output",  "Human features"],horizontal=True,
    captions = ["Model results", "Roads and towns"])

if map_view == 'Model output': 
  m=level1_boundary.explore()
  st_folium(m, width=725)
elif map_view == 'Human features':
  m = level1_boundary.boundary.explore(color = 'black')
  m = towns.explore(m=m)
  m = roads.explore(m=m, color='red')
  st_folium(m, width=725)


st.image(['./UKRI_STFC_HARTREE_CENTRE_RGB.png','./UN_Datathon_logo_with_text.png'], width=150)
