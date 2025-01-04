from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables
import folium
import streamlit as st
import os
import psycopg2
import pandas as pd
import google.generativeai as genai
from streamlit_folium import st_folium
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://dbpedia.org/sparql")
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response


def execute_sparql_query(query):
    # Define the DBpedia SPARQL endpoint URL
    sparql_endpoint = "https://dbpedia.org/sparql"
    
    # Create an instance of SPARQLWrapper with the DBpedia endpoint
    sparql = SPARQLWrapper(sparql_endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        # Execute the query and get the results in JSON format
        results = sparql.query().convert()
        st.write(results)
        # Iterate over and print each result
        for result in results["results"]["bindings"]:
            print(result)
            st.write(result)
    except Exception as e:
        print(f"An error occurred while executing the query: {e}")

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

    
def get_gemini_present(question,response,display):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([display[0],response[0]])
    st.write(response.text)
    #return response.text
def create_map(data):
    # Create a Folium map centered at a specific location
    m = folium.Map(location=[20, 0], zoom_start=2)  # Center of the world map

    # Add points to the map
    for name, geom in data:
        lon, lat = map(float, geom.replace('POINT(', '').replace(')', '').split())
        folium.Marker(
            location=[lat, lon],  # Latitude and longitude
            popup=name,  # Display name on marker click
        ).add_to(m)

    return m

## Define Your Prompt
prompt=[
    """
You are an expert in converting English questions into SPARQL queries to retrieve information from DBpedia!

Your task is to analyze the user's natural language question, understand its context, and convert it into a valid SPARQL query that can be executed against the DBpedia knowledge base. Ensure the generated queries follow the correct syntax, include relevant prefixes, and handle various data types like literals, URIs, and properties efficiently.

## Guidelines:
1. Identify the entities, classes, and properties mentioned in the question.
2. Map them to corresponding resources in DBpedia, using appropriate prefixes like `dbo:`, `dbr:`, and `rdf:`.
3. Construct a query that includes `SELECT`, `WHERE`, and any necessary `FILTER` or `ORDER BY` clauses.
4. If the question is ambiguous, create a query that returns broader results with a limit clause (e.g., `LIMIT 10`).


## Examples:
 Example 1:
User Query: ""What is the capital of France?""
SPARQL Query:
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT ?capital WHERE {
  dbr:France dbo:capital ?capital .
}

    """


]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    #print(response)
    #response=get_postgre_data(response)
    st.subheader("Response:")
    st.write(response)
    execute_sparql_query(response)

    










