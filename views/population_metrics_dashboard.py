import pyproj
import streamlit as st 
import pandas as pd 
import geopandas as gpd 
import plotly.express as px 
from matplotlib import pyplot as plt
import json

@st.cache_data()
def load_data():
    df = pd.read_csv('datasets/kenya-population-distribution-2019-updated.csv')
    gd = gpd.read_file('datasets/kenya-counties-geopandas-updated-merged.shp')
    geo_json_file = 'datasets/kenya-counties-geopandas-geojson.json'
    return df, gd,geo_json_file

df, gd, geo_json_file = load_data()

new_gd = gd[['County', 'Male', 'Female', 'Intersex', 'Total', 'Percentage','PERIMETER' ,'AREA','geometry', 'OBJECTID']]

data_gd = gd[['County', 'Male', 'Female', 'Intersex', 'Total', 'Percentage']]


geo_json = json.loads(gd.to_json())


st.title('📈Population Metrics Dashboard')

#STEP 1: HEADER TEXT ON DATASET 
st.header('Dataset: Kenya Population Distribution 2019 Census')

#STEP 2: BASIC DESCRIPTION OF THE DATASET
st.markdown(
    """
        ### Population Metrics

        The dataset contains the distribution of population in Kenya based on the census
        conducted in 2019.

        Source: [Kaggle] https://www.kaggle.com/datasets/paulmaluki/kenyapopulationdistibution-2019-censuscsv?resource=download

        Date of Analysis: 2022-03-29

        Purpose of Analysis: Learning basic methodologies of data analysis in Python, Data Cleaning,
        and EDA

        Dataset Description:
        The dataset focuses on the population distribution of the country in 2019.
        Kenya is divided into 47 counties. The dataset contains the following variables:
        - county
        - total population
        - male
        - female
        - intersex
        - percentage (% of total population)

    """
)

st.header('📅 Data Table')

if 'selected_counties' not in st.session_state:
    st.session_state.selected_counties = new_gd['County'].unique().tolist()

selected_counties = st.multiselect(
    'Select County',
    new_gd['County'].unique(),
    default=new_gd['County'].unique()
)


filtered_gd = new_gd[new_gd['County'].isin(selected_counties)]

if selected_counties: 

    county_name =', '.join( filtered_gd['County'].unique())
    total_population = filtered_gd['Total'].sum()
    total_male = filtered_gd['Male'].sum()
    total_female = filtered_gd['Female'].sum()
    total_intersex = filtered_gd['Intersex'].sum()
    total_perimeter = filtered_gd['PERIMETER'].sum()
    total_area = filtered_gd['AREA'].sum()
    mean_population_density = filtered_gd['Total'].sum() / filtered_gd['AREA'].sum()
    ratio_of_male_to_female = total_male / total_female
    ratio_of_female_to_male = total_female / total_male
    mean_area = filtered_gd['AREA'].mean()
    median_area = filtered_gd['AREA'].median()

else: 
    county_name = 'Kenya Total'
    area_name = 'Kenya Area'
    perimeter_name = 'Kenya Perimeter'
    total_population = new_gd['Total'].sum()
    total_male = new_gd['Male'].sum()
    total_female = new_gd['Female'].sum()
    total_intersex = new_gd['Intersex'].sum()
    total_perimeter = new_gd['PERIMETER'].sum()
    total_area = new_gd['AREA'].sum()
    mean_population_density = new_gd['Total'].sum() / new_gd['AREA'].sum()
    ratio_of_male_to_female = total_male / total_female
    ratio_of_female_to_male = total_female / total_male
    mean_area = new_gd['AREA'].mean()
    median_area = new_gd['AREA'].median()


col1, col2, col3 = st.columns(3, gap='small', vertical_alignment='top')

with col1:
    st.subheader('Totals', divider=True)
    st.metric(label="Total Population", value=f"{total_population:,}")
    
with col2: 
    st.subheader('Area / Perimeter', divider=True)
    st.metric(label="Total Area", value=f"{total_area:,.2f}SQ.KM")
    st.metric(label="Total Perimeter", value=f"{total_perimeter:,.2f}KM")
with col3: 
    st.subheader('Density', divider=True)
    st.metric(label="Mean Population Density", value=f"{mean_population_density:,.2f}")
    
st.markdown("------")
st.markdown(
    f"""
    <h4>
        County:
    </h4>
    <p>{county_name}</p>
""", unsafe_allow_html=True
)
st.markdown('--------')



st.header('🗺 Kenya Choropleth Map')


if selected_counties:
    st.dataframe(filtered_gd[['County', 'Male', 'Female', 'Intersex', 'Total', 'Percentage', 'PERIMETER', 'AREA']], width=1000, hide_index=True)

else:
    st.dataframe(new_gd[['County', 'Male', 'Female', 'Intersex', 'Total', 'Percentage', 'PERIMETER', 'AREA']], width=1000, hide_index=True)



gd_columns = new_gd.columns.to_list()

selected_field = st.selectbox(
    'Select Field',
    gd_columns[1:8],
    index=0
)

st.write('\n')

fig = px.choropleth(
    new_gd, 
    title=f'Kenya Population Distribution 2019 Census Choropleth Map: {selected_field}',
    geojson=geo_json,
    locations=new_gd.index,
    width=800,
    height=600,
    color= selected_field,
    color_continuous_scale='Blues',
    hover_name='County',
    hover_data={
        'Total': True, 
        'Male' : True,
        'Female' : True,
        'Intersex' : True,
        'Percentage' : True,
        'PERIMETER' : True,
        'AREA' : True
        },
    projection='mercator'
)
fig.update_geos(fitbounds="locations", visible=False)

fig.update_layout(
    coloraxis_colorbar=dict(
        title=f'{selected_field}',
        ticks = 'outside', 
        tickvals = [new_gd[selected_field].min(), new_gd[selected_field].max()],
        ticktext = [f'{new_gd[selected_field].min()}', f'{new_gd[selected_field].max()}'],
    ),
     paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
    plot_bgcolor='rgba(0,0,0,0)'    # Transparent plot background
)

st.plotly_chart(fig)


# BAR CHART
st.write('\n')

st.header('📈 Population Metrics Bar Chart')
# lets make selected_field dynamic where selecting a field changes the min and max slider


#create a min and max st slider 
min_value = st.slider('Min Total Population', min_value=int(new_gd['Total'].min()), max_value=int(new_gd['Total'].max()), value=int(new_gd['Total'].min()))
max_value = st.slider('Max Total Population', min_value=int(new_gd['Total'].min()), max_value=int(new_gd['Total'].max()), value=int(new_gd['Total'].max()))

filtered_bar_gd = new_gd[(new_gd['Total'] >= min_value) & (new_gd['Total'] <= max_value)]

st.write(f'\nShowing results between: {f'{min_value:,}'} and {f'{max_value:,}'}')

st.dataframe(
    filtered_bar_gd[['County','Male','Female','Intersex','Total','Percentage', 'PERIMETER', 'AREA']],
    width=1000,
    hide_index=True
)


fig = px.bar(
    filtered_bar_gd,
    title= f'Kenya Population Distribution 2019 Census Bar Chart: {selected_field}',
    x = 'County',
    y = selected_field,
    color_discrete_map={
        'Male' : 'blue',
        'Female' : 'red',
        'Intersex' : 'green'
    },
    color = 'Percentage',
    hover_data=['Total', 'PERIMETER', 'AREA'],
)

st.plotly_chart(fig)