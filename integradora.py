import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go

st.title("Detection and prediction of crimes")
st.subheader('San Francisco City Council and Police Department')
df = pd.read_csv('Police_Department_Incident_Reports__2018_to_Present.csv')

#Tratamiento de nulos
df=df.dropna(how='all',axis=0)
df=df.dropna(how='all',axis=1)
#df.head()

#Tratamiento de columnas 
df.drop(['HSOC Zones as of 2018-06-05', 'OWED Public Spaces', 'Central Market/Tenderloin Boundary Polygon - Updated','Parks Alliance CPSI (27+TL sites)','ESNCAG - Boundary File','Areas of Vulnerability, 2016'],inplace=True, axis=1)


#Datasets para el top 5
Larceny = pd.read_csv('Larceny.csv')
Assault = pd.read_csv('Assault.csv')
Burglary = pd.read_csv('Burglary.csv')
MV_Theft = pd.read_csv('MV_Theft.csv')
Fraud = pd.read_csv('Fraud.csv')

#Datasets para los años
Year_2018 = pd.read_csv('Year_2018.csv')
Year_2019 = pd.read_csv('Year_2019.csv')
Year_2020 = pd.read_csv('Year_2020.csv')

#Dataset para los historicos
Semes1=pd.read_excel('1erS_2018.xlsx')
Semes2=pd.read_excel('2doS_2018.xlsx')
Semes1_2019=pd.read_excel('1erS_2019.xlsx')
Semes2_2019=pd.read_excel('2doS_2019.xlsx')
Semes1_2020=pd.read_excel('1erS_2020.xlsx')


#Menú interactivo con streamlit
st.sidebar.checkbox("Analysis by incident", True, key = 1)
category=df['Incident Category'].unique()

selected_status = st.sidebar.selectbox('Incidents category',
                                       options=['Interactive Map', 
                                                'Top 5 (Neighborhood)',
                                                'Top 5 incidents per year',
                                                'Incidents by day of week','Historical'])
#Gráficos con plotly

#Opcion 1 "Mapa interactivo"
if selected_status == 'Interactive Map':
    fig= px.scatter_mapbox(df,
                           lon = df['Longitude'],
                           lat = df['Latitude'],
                           zoom = 8,
                           color = df ['Analysis Neighborhood'],
                           width = 900,
                           height= 600,
                           title = 'Risk neighborhoods (2018-2020)'
                              )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0, "t":50, "l":0, "b":10})
    st.plotly_chart(fig)
    
#Opcion 2 "Top 5 por Incident Category"

if selected_status == 'Top 5 (Neighborhood)':
    
    st.markdown ('Analysis by neighborhood during 2018-2020 with the most important categorical incidents (ordered)')
    
    fig= px.histogram(Larceny, x='Analysis Neighborhood', color='Incident Category')
    st.plotly_chart(fig)
    
    fig= px.histogram(Assault, x='Analysis Neighborhood', color='Incident Category')
    st.plotly_chart(fig)
    
    fig= px.histogram(Burglary, x='Analysis Neighborhood', color='Incident Category')
    st.plotly_chart(fig)
    
    fig= px.histogram(MV_Theft, x='Analysis Neighborhood', color='Incident Category')
    st.plotly_chart(fig)
    
    fig= px.histogram(Fraud, x='Analysis Neighborhood', color='Incident Category')
    st.plotly_chart(fig)
    
    
#Opcion 3 "Filtro por año para el top 5 de Incident Category"
Category_2018=Year_2018['Incident Category'].value_counts()
Category_2019=Year_2019['Incident Category'].value_counts()
Category_2020=Year_2020['Incident Category'].value_counts()

    
if selected_status == 'Top 5 incidents per year':
    fig= px.bar(Category_2018, x=Category_2018.index, y=Category_2018.values,height=500)
    
    fig.update_layout(title='Top 5 by Category Incident in 2018',
                      xaxis_title='Category',yaxis_title='Count')
    st.plotly_chart(fig)
    
    fig= px.bar(Category_2019, x=Category_2019.index, y=Category_2019.values, height=500)
    fig.update_layout(title='Top 5 by Category Incident in 2019',
                      xaxis_title='Category',yaxis_title='Count')
    st.plotly_chart(fig)
    
    fig= px.bar(Category_2020, x=Category_2020.index, y=Category_2020.values, height=500)
    fig.update_layout(title='Top 5 by Category Incident in 2020',
                      xaxis_title='Category',yaxis_title='Count')
    st.plotly_chart(fig)
    
    
#Opcion 4 "Filtro por dia de la semana"
D_Week_2018=Year_2018['Incident Day of Week'].value_counts()
D_Week_2019=Year_2019['Incident Day of Week'].value_counts()
D_Week_2020=Year_2020['Incident Day of Week'].value_counts()


if selected_status == 'Incidents by day of week':
    fig = px.line(D_Week_2018, x=D_Week_2018.index, y=D_Week_2018.values)
    fig.update_layout(title='Incident by Day of Week 2018',
                      xaxis_title='Day of Week',yaxis_title='Count')
    st.plotly_chart(fig)
    
    fig = px.line(D_Week_2019, x=D_Week_2019.index, y=D_Week_2019.values)
    fig.update_layout(title='Incident by Day of Week 2019',
                      xaxis_title='Day of Week',yaxis_title='Count')
    st.plotly_chart(fig)
    
    fig = px.line(D_Week_2020, x=D_Week_2020.index, y=D_Week_2020.values)
    fig.update_layout(title='Incident by Day of Week 2020',
                  xaxis_title='Day of Week',yaxis_title='Count')
    st.plotly_chart(fig)

    
#Opción 5 "Historicos"

#Value counts (scatter)
S1_2018 = Semes1['Incident Date'].value_counts()
S2_2018 = Semes2['Incident Date'].value_counts()
S1_2019 = Semes1_2019['Incident Date'].value_counts()
S2_2019 = Semes2_2019['Incident Date'].value_counts()
S1_2020 = Semes1_2020['Incident Date'].value_counts()

#Value counts (Pie)
Top_5_2018=Year_2018['Incident Category'].value_counts()
Top_5_2019=Year_2019['Incident Category'].value_counts()
Top_5_2020=Year_2020['Incident Category'].value_counts()

#Filtro proximidad (Latitud y longitud)
PD_Coord=df.groupby("Police District").aggregate(Lat=("Latitude", "median"),Lon=("Longitude","median"))


if selected_status == 'Historical':
    #Primer Sem 2018
    st.markdown ('Number of incidents by date (divided by semesters)')

    fig= px.scatter(S1_2018, y=S1_2018.values, x=S1_2018.index,
                    size=S1_2018.values, height=700)
    fig.update_layout(title='Incidents in 2018',
                      xaxis_title='First semester',
                      yaxis_title='Count')
    st.plotly_chart(fig)
    
    #Segundo Sem 2018
    fig= px.scatter(S2_2018, y=S2_2018.values, x=S2_2018.index, 
                    size=S2_2018.values, height=700)
    fig.update_layout(title='Incidents in 2018',
                      xaxis_title='Second semester',
                      yaxis_title='Count')

    st.plotly_chart(fig)
    #st.markdown ('Number of incidents by date (divided by semesters)')

    
    #Primer Sem 2019
    fig= px.scatter(S1_2019, y=S1_2019.values, x=S1_2019.index, size=S1_2019.values
                    ,height=700)
    fig.update_layout(title='Incidents in 2019',
                      xaxis_title='First semester',
                      yaxis_title='Count')

    st.plotly_chart(fig)
    
    #Segundo Sem 2019
    fig= px.scatter(S2_2019, y=S2_2019.values, x=S2_2019.index, size=S2_2019.values,
                    height=700)
    fig.update_layout(title='Incidents in 2019',
                      xaxis_title='Second semester',
                      yaxis_title='Count')

    st.plotly_chart(fig)
    
    #Primer Sem 2020
    fig= px.scatter(S1_2020, y=S1_2020.values, x=S1_2020.index, size=S1_2020.values,
                    height=700)
    fig.update_layout(title='Incidents in 2020',
                      xaxis_title='First semester',
                      yaxis_title='Count')

    st.plotly_chart(fig)

    
      
    #2018 Pie
    fig = px.pie(Top_5_2018, values=Top_5_2018.values, 
                 names=Top_5_2018.index, 
                 title='Probability of incidents in 2018')
    st.plotly_chart(fig)
    
    #2019 Pie
    fig = px.pie(Top_5_2019, values=Top_5_2019.values, 
                 names=Top_5_2019.index, 
                 title='Probability of incidents in 2019')
    st.plotly_chart(fig)

    #2020 Pie
    fig = px.pie(Top_5_2020, values=Top_5_2020.values, 
                 names=Top_5_2020.index, 
                 title='Probability of incidents in 2020')
    
    st.plotly_chart(fig)
    
    #Proximidad de latitud y longitud

    fig= px.scatter(PD_Coord, y=PD_Coord['Lat'], x=PD_Coord['Lon'], color=PD_Coord.index)
    fig.update_layout(title='Latitude and Longitude Proximity', xaxis_title='Longitude', yaxis_title='Latitude')
    st.plotly_chart(fig)
    st.markdown ('Proximity of latitude and longitude taking into account the median')
    

    



