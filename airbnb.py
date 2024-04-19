import pandas as pd 
import pymongo
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.express as px 
import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu



# connection to mongodb
client = pymongo.MongoClient("mongodb+srv://lavanya:Lavan123@guvilavan.5pjwpvl.mongodb.net/?retryWrites=true&w=majority")
db = client['sample_airbnb']
col = db['listingsAndReviews']


def data():
    clm = {'name': [], 'country': [], 'property_type': [], 'price': [], 'room_type': [],
           'bedrooms': [], 'beds': [],'accommodates':[],'cancellation_policy': [],'number_of_reviews': [],
           'minimum_nights': [], 'extra_people':[],'maximum_nights': [],'guests_include': [],'review_scores_cleanliness': [],
           'last_scraped': [], 'host_name':[], 'host_listings_count':[],'calendar_last_scraped': [], 
           'availability_365': [],'latitude': [], 'longitude': []}

    for i in col.find():
        name = i.get('name')
        country = i['address'].get('country')
        property_type = i.get('property_type')
        price = i.get('price')
        room_type = i.get('room_type')

        accommodates = i.get('accommodates')
        minimum_nights = i.get('minimum_nights')
        maximum_nights = i.get('maximum_nights')
        cancellation_policy = i.get('cancellation_policy')
        number_of_reviews = i.get('number_of_reviews')

        bedrooms = i.get('bedrooms')
        beds = i.get('beds')
        guests_include = i.get('guests_included')
        extra_people = i.get('extra_people')
        review_scores_cleanliness = i['review_scores'].get('review_scores_cleanliness')
        last_scraped = i.get('last_scraped')
        
        host_name = i['host'].get('host_name')
        host_total_listings = i['host'].get('host_total_listings_count')
        calendar_last_scraped = i.get('calendar_last_scraped')
        availability_365 = i['availability'].get('availability_365')
        latitude = i['address']['location'].get('coordinates')[0]
        longitude = i['address']['location'].get('coordinates')[1]

        clm['name'].append(name)
        clm['country'].append(country)
        clm['property_type'].append(property_type)
        clm['price'].append(price)
        clm['room_type'].append(room_type)

        clm['accommodates'].append(accommodates)
        clm['minimum_nights'].append(minimum_nights)
        clm['maximum_nights'].append(maximum_nights)
        clm['number_of_reviews'].append(number_of_reviews)
        clm['cancellation_policy'].append(cancellation_policy)

        clm['bedrooms'].append(bedrooms)
        clm['beds'].append(beds)
        clm['guests_include'].append(guests_include)
        clm['extra_people'].append(extra_people)
        clm['review_scores_cleanliness'].append(review_scores_cleanliness)
        clm['last_scraped'].append(last_scraped)
        
        clm['host_name'].append(host_name)
        clm['host_listings_count'].append(host_total_listings)
        clm['availability_365'].append(availability_365)
        clm['calendar_last_scraped'].append(calendar_last_scraped)
        clm['latitude'].append(latitude)
        clm['longitude'].append(longitude)

    df = pd.DataFrame(clm)
    #data cleaning
    df['review_scores_cleanliness'] = df['review_scores_cleanliness'].fillna(0)
    df['beds'] = df['beds'].fillna(1)
    df['bedrooms'] = df['bedrooms'].fillna(1)
    df['last_scraped'] = df['last_scraped'].dt.date
    df['calendar_last_scraped'] = df['calendar_last_scraped'].dt.date
    df.dropna(inplace=True)
    return df


#dataframe
df = pd.read_csv('C:/Users/DELL/Desktop/Project4-Airbnb/records2')
df.drop('Unnamed: 0', axis=1, inplace=True)
df.dropna(inplace=True)
#Streamlit page
st.set_page_config(layout= "wide")

# Using st.markdown with right alignment
#st.markdown("<h1 style='text-align: right; color: black;'>Airbnb Analysis</h1>", unsafe_allow_html=True)
#st.markdown("<h2 style='text-align: right; color: blue;'>Airbnb Property Type Visualization</h2>", unsafe_allow_html=True)


st.markdown(f""" <style>.stApp {{
                    background: url('https://www.hotelnewsnow.com/Media/Default/Legacy/FeatureImages/20160209_STR_Airbnb_Feature_Headline1.jpg');   
                    background-size: cover}}
                 </style> """,unsafe_allow_html=True)


option = st.sidebar.radio(":blue[Choose your page]", ["Home", "Data Visualization"])
    
if option == "Home":
    st.markdown("<h1 style='text-align: right; color: black;'>Airbnb Analysis</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col2:
        st.image("C:/Users/DELL/Pictures/1.webp",width=600)

    

if option == 'Data Visualization':
    st.markdown("<h1 style='text-align: right; color: black;'>Airbnb Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: right; color: blue;'>Airbnb Property Type Visualization</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)
    col9, col10 = st.columns(2)
    with col1:
        # Choose a country
        st.markdown('<h2 style="color: black;">Select a country</h2>', unsafe_allow_html=True)

        selected_country = st.selectbox("", df['country'].unique())
        
        # Filter data based on selected country
        filtered_df = df[df['country'] == selected_country]

    with col3:
        
        # Group by property type and sum the number_of_reviews
        property_reviews = filtered_df.groupby('property_type')['number_of_reviews'].sum().reset_index()

        # Sort the values by number_of_reviews in descending order
        property_reviews = property_reviews.sort_values(by='number_of_reviews', ascending=False)

        # Get top 10 property types
        top_10_property_reviews = property_reviews.head(10)

        # Plot countplot using Plotly
        fig = px.bar(top_10_property_reviews, 
                    x='property_type', 
                    y='number_of_reviews', 
                    color='property_type')
        fig.update_layout(title='Top 10 Property Types in {} by Number of Reviews'.format(selected_country),
                        xaxis_title='Property Type', 
                        yaxis_title='Number of Reviews')
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        df_avg_price = df.groupby('property_type')['price'].mean().reset_index()
        df_avg_price = df_avg_price.sort_values(by='price', ascending=False).head(15)

        # Create a Plotly bar plot using the top 15 property types by average price
        fig = px.bar(
            df_avg_price,
            x='property_type',
            y='price',
            color='price',
            color_continuous_scale='viridis',
            title='Average Price by Property Type (Top 15)',
            labels={'property_type': 'Property Type', 'price': 'Average Price'}
        )

        # Customize the layout of the Plotly figure
        fig.update_layout(
            xaxis_title='Property Type',
            yaxis_title='Average Price',
            xaxis_tickangle=-45,
            coloraxis_colorbar=dict(title='Price', tickprefix='$')
        )

        # Render the Plotly figure in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    with col4:
        
        
        # Group by property type and calculate the mean review score for cleanliness
        property_cleanliness = filtered_df.groupby('property_type')['review_scores_cleanliness'].sum().reset_index()

        # Sort the values by mean review score in descending order
        property_cleanliness = property_cleanliness.sort_values(by='review_scores_cleanliness', ascending=False)

        # Get top 5 property types
        top_5_property_cleanliness = property_cleanliness.head(5)

        # Plot pie chart using Plotly
        fig = px.pie(top_5_property_cleanliness, 
                    values='review_scores_cleanliness', 
                    names='property_type',
                    title='Top 5 Property Types with Highest Review Scores for Cleanliness in {}'.format(selected_country))
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        # Aggregate data by country
        country_agg = df.groupby('country').agg({'price': 'mean'}).reset_index()

        # Create choropleth map
        fig = px.choropleth(country_agg, 
                            locations='country', 
                            locationmode='country names',
                            color='price', 
                            hover_name='country',
                            color_continuous_scale='Viridis',
                            title='Average Price by Country')
        st.plotly_chart(fig)

    with col8:
        col1, col2 = st.columns(2)
        with col1:
            # Define the desired price range for the slider (0 to 3000)
            price_min = 0
            price_max = 3000

            # User input for price range
            st.markdown('<h2 style="color: black;">Select a price range</h2>', unsafe_allow_html=True)
            price_range = st.slider("Select price range", price_min, price_max, (price_min, price_max))

            # Filter the DataFrame based on the selected price range
            filtered_df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]
        
    with col7:
        
        # User input for the number of beds, bedrooms, and cancellation policy
        st.markdown('<h2 style="color: black;">Choose additional filters</h2>', unsafe_allow_html=True)
        col3, col4 ,col5= st.columns(3)
        with col3:
            selected_beds = st.selectbox("Number of beds", options=sorted(filtered_df['beds'].unique()))
        with col4:
            selected_bedrooms = st.selectbox("Number of bedrooms", options=sorted(filtered_df['bedrooms'].unique()))
        with col5:
            selected_cancellation_policy = st.selectbox("Cancellation policy", options=filtered_df['cancellation_policy'].unique())
    with col9:
        # Filter the DataFrame based on the user's selections
        filtered_df = filtered_df[
        (filtered_df['beds'] == selected_beds) &
        (filtered_df['bedrooms'] == selected_bedrooms) &
        (filtered_df['cancellation_policy'] == selected_cancellation_policy)]

        
        # Find the top 10 apartment names based on the filtered DataFrame
        top_10_names = filtered_df['name'].value_counts().head(10).index

        # Filter the DataFrame to include only the top 10 names
        filtered_top_10_df = filtered_df[filtered_df['name'].isin(top_10_names)]

        # Truncate apartment names to a specified length (e.g., 15 characters)
        max_name_length = 15
        filtered_top_10_df['name_truncated'] = filtered_top_10_df['name'].apply(lambda x: x[:max_name_length] + '...' if len(x) > max_name_length else x)

        # Plot the bar plot of the top 10 apartment names within the selected filters using truncated names
        fig = px.bar(
            filtered_top_10_df,
            x='name_truncated',
            y='price',
            title=f'Top 10 Apartment Names within Selected Filters',
            labels={'name_truncated': 'Apartment Name', 'price': 'Price'},
            hover_data=['name','number_of_reviews', 'review_scores_cleanliness']
        )

        # Customize layout and display the Plotly chart in Streamlit
        fig.update_layout(
            xaxis_title='Apartment Name',
            yaxis_title='Price'
        )
        st.plotly_chart(fig, use_container_width=True)