
# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Setting up page configuration
icon = Image.open("airbnb.png")
st.set_page_config(page_title= "Airbnb Data Visualization",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Jafar Hussain*!
                                        Data has been gathered from mongodb atlas"""}
                  )

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Overview","Explore"], 
                           icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}
                          )

# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.sample_airbnb
col = db.listingsAndReviews

# READING THE CLEANED DATAFRAME
df = pd.read_csv('Airbnb_data.csv')

# HOME PAGE
if selected == "Home":
    # Content
    st.image("airbnb_1.png")
    st.markdown("#")
    st.markdown("## :blue[About] : Airbnb, Inc. ( AIR-BEE-en-BEE) is an American company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. Airbnb is the most well-known company for short-term housing rentals.")
    st.markdown("#")
   
    

    
# OVERVIEW PAGE
if selected == "Overview":
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country', sorted(df.Country.unique()), sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type', sorted(df.Property_type.unique()), sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type', sorted(df.Room_type.unique()), sorted(df.Room_type.unique()))
    price = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()))

    # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

    # CREATING COLUMNS
    col1, col2 = st.columns(2, gap='medium')

    with col1:
        # TOP 10 PROPERTY TYPES BAR CHART
        df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
        fig = px.bar(df1,
                     title='Top 10 Property Types',
                     x='Listings',
                     y='Property_type',
                     orientation='h',
                     color='Property_type',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

        # TOP 10 HOSTS BAR CHART
        df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
        fig = px.bar(df2,
                     title='Top 10 Hosts with Highest number of Listings',
                     x='Listings',
                     y='Host_name',
                     orientation='h',
                     color='Host_name',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
        df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
        fig = px.pie(df1,
                     title='Total Listings in each Room_types',
                     names='Room_type',
                     values='counts',
                     color_discrete_sequence=px.colors.sequential.Rainbow
                     )
        fig.update_traces(textposition='outside', textinfo='value+label')
        st.plotly_chart(fig, use_container_width=True)

        # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
        country_df = df.query(query).groupby(['Country'], as_index=False)['Name'].count().rename(columns={'Name': 'Total_Listings'})
        fig = px.choropleth(country_df,
                            title='Total Listings in each Country',
                            locations='Country',
                            locationmode='country names',
                            color='Total_Listings',
                            color_continuous_scale=px.colors.sequential.Plasma
                            )
        st.plotly_chart(fig, use_container_width=True)

        
# EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")
    
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    # HEADING 1
    st.markdown("## Price Analysis")
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')
    
    with col1:
        
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=pr_df,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
        # HEADING 2
        st.markdown("## Availability Analysis")
        
        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(query),
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room_type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    with col2:
        
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Price', 
                                       hover_data=['Price'],
                                       locationmode='country names',
                                       size='Price',
                                       title= 'Avg Price in each Country',
                                       color_continuous_scale='agsunset'
                            )
        col2.plotly_chart(fig,use_container_width=True)
        
        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")
        
        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Availability_365', 
                                       hover_data=['Availability_365'],
                                       locationmode='country names',
                                       size='Availability_365',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)
        
        
        
        
        
        
        
