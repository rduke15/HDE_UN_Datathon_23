import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium
import geopandas

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    # set up sidebar
    st.sidebar.markdown(
        "Click the pages above to explore"
    )
    st.sidebar.image('rising_logo.png')

    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    # start page
    st.title("Counties Data")
    
    # read in data
    counties_list = pd.read_csv("./Datasets/gdp_county_2017.csv")
    counties_list = counties_list['County'].to_list()
    model_predictions = pd.read_csv("./model_outputs/all_counties_predictions.csv")
    
    # create county selection box
    county = st.selectbox(
        "Please select the county to explore", 
        counties_list,
        index=None,
        placeholder="Select county...",
    )

    # if county is selected plot data for that county
    if county:
        county = county.replace('County', '')
        county = county.replace('county', '')
        county = county.lower()
        county = county.strip()

        st.header("Model prediction")

        col1, col2 = st.columns(2)
        with col1:
            level1_boundary = geopandas.read_file("./Datasets/Shape_files/ken_adm_iebc_20191031_shp/ken_admbnda_adm1_iebc_20191031.shp")
            county_map = level1_boundary[level1_boundary['ADM1_EN'].str.lower()==county]
            m=county_map.explore()
            st_folium(m, height=250, width=400)

        with col2:
            st.table(model_predictions.loc[model_predictions['county']==county, ['county','true_value','prediction']])


        st.markdown('''**Explanation of model predictions:**  
                    Lime values for the model, showing positive and negative contributions.  
                    Positive contributions will increase the GDP and negative contributions will decrease  
                    The value is the value of the scaled model inputs (these can be converted back to real values )''')
     
        with open(f"./model_outputs/lime_explainations/{county}_explaination.html", 'r', encoding='utf-8') as HtmlFile:
            source_code = HtmlFile.read() 
            components.html(source_code,height = 350,width=1000)
        
        st.subheader("Top 3 influencing features")
        st.markdown('''Increasing negative influences will improve the GDP ''')
        lime_values = pd.read_csv(f"./model_outputs/lime_explainations/{county}_lime_values.csv")
        lime_values = lime_values[['0','1']]
        lime_values = lime_values.rename(columns={'0':'feature_values'})
        st.table(lime_values.loc[0:2,'feature_values'])
        
    st.image(['./Data_app/UKRI_STFC_HARTREE_CENTRE_RGB.png','./Data_app/UN_Datathon_logo_with_text.png'], width=150)