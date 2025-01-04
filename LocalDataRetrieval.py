from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables
import streamlit as st
import os
import psycopg2
import pandas as pd
import google.generativeai as genai


## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def get_postgre_data(query):
    try:
        # Connect to your PostgreSQL/PostGIS database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="//give own password",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)
        return rows
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


## Define Your Prompt
prompt=[
    """
You are an expert in converting English questions to SQL queries!

The SQL database has multiple tables with geospatial data. Here are some of the tables and their columns:

attractions:

attraction_id
name
description
category
location (geography type)
routes:

route_id
route_name
description
route_type
path (geography type)
accommodations:

accommodation_id
name
address
type
price_per_night
rating
location (geography type)
points_of_interest:

poi_id
name
type
description
location (geography type)
Here are some example questions and their corresponding SQL queries:

Example 1: How many tourist attractions are there in the database?
The SQL command will be something like this:
SELECT COUNT(*) FROM tourism.attractions;

Example 2: Find the nearest tourist attraction to a given point (-73.9900, 40.7500).
The SQL command will be something like this:
SELECT name, description, ST_Distance(location, ST_GeogFromText('POINT(-73.9900 40.7500)')) AS distance FROM tourism.attractions ORDER BY distance LIMIT 5;

Example 3: Show all accommodations within a 2 km radius of a given point (-73.9851, 40.7580).
The SQL command will be something like this:
SELECT name, address, price_per_night, rating FROM tourism.accommodations WHERE ST_DWithin(location, ST_GeogFromText('POINT(-73.9851 40.7580)'), 2000);

Example 4: Find all routes that pass near Central Park within 500 meters.
The SQL command will be something like this:
SELECT route_name, description FROM tourism.routes WHERE ST_DWithin(path, (SELECT location FROM tourism.attractions WHERE name = 'Central Park'), 500);

Example 5: Find tourist attractions within a 1 km buffer zone around Central Park.
The SQL command will be something like this:
SELECT name, description FROM tourism.attractions WHERE ST_DWithin(location, (SELECT location FROM tourism.attractions WHERE name = 'Central Park'), 1000);

Note: The SQL result should not have any special formatting like ``` or sql at the beginning or ending.

    """


]


## Streamlit App

st.set_page_config(page_title="Spatial Mind", page_icon="🌍", layout="centered")
# App Header
st.title("🌍 Spatial Mind")
st.subheader("Unlock the Power of Geospatial Data!")
st.markdown("---")

# Sidebar Info
st.sidebar.header("🔍 What is Spatial Mind?")
st.sidebar.info(
    """
    **Spatial Mind** uses Google Gemini to analyze geospatial data or convert English questions into SPARQL/SQL queries.
    
    💡 You can:
    - Ask questions about geospatial locations.
    - Convert natural language questions into executable SPARQL/SQL queries.
    """
)
st.sidebar.markdown("---")

# Sidebar for Database Selection (placed below the existing info)
st.sidebar.header("🌐 Choose a Database")
selected_db = st.sidebar.radio(
    "Select the database to query:",
    ("Local Database", "Open source Data")
)

    

# Input Section
st.write("### Ask Your Question")
st.write("Enter your  query below and get results fetched from local database.")
question = st.text_input("Type your question here:", key="input", placeholder="e.g., What is the capital of France?")



# Submit Button with custom style
submit = st.button("🔍 Fetch data", help="Click to process your query")

# if submit is clicked
if submit:
    st.write("### 🧠 SQL Query")
    with st.spinner('🔍 Generating SQL query...'):
        response = get_gemini_response(question, prompt)
        st.code(response, language="sql")
    
    st.markdown("---")
    st.write("### 📍 Raw data:")
    with st.spinner('🌍 Retrieving geospatial data...'):
            response=get_gemini_response(question,prompt)
            response=get_postgre_data(response)
            st.success("Geospatial data retrieved successfully!")
            st.write(response)


    if response:
        
        try:
            # Directly convert response to a DataFrame if it's a list of lists or similar
            df = pd.DataFrame(response)
            
            # Optionally, set column names
            df.columns = [f'Column {i+1}' for i in range(len(df.columns))]
            
            # Display the DataFrame
            st.write("### Data Table:")
            st.table(df)  # Static table
        
            
        except Exception as e:
            st.write(f"Error creating DataFrame: {e}")
        
    else:
        st.write("No data available.")


st.markdown(
    """
    ---
    <div style='text-align: center; font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; color: #4a4a4a;'>
        <p> <span style='font-style: italic;'>Rahshana K</span> & <span style='font-style: italic;'>Athirai</span> 🎓</p>
        
    </div>
    """, unsafe_allow_html=True
)











