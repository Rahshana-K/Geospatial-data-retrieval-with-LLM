from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables
import streamlit as st
import os
import google.generativeai as genai

# Configure GenAI API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to Load Google Gemini Model and Provide Queries as Response
def get_gemini_prompt(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Define Prompts
prompt = [
    """
You are an expert in retrieving geospatial data and answering geospatial-related queries.
All queries asked are geospatial-related queries.
    """
]

S_prompt = [
    """
You are an expert in converting English questions into SPARQL queries to retrieve information from DBpedia!

Your task is to analyze the user's natural language question, understand its context, and convert it into a valid SPARQL query that can be executed against the DBpedia knowledge base. Ensure the generated queries follow the correct syntax, include relevant prefixes, and handle various data types like literals, URIs, and properties efficiently.

## Guidelines:
1. Identify the entities, classes, and properties mentioned in the question.
2. Map them to corresponding resources in DBpedia, using appropriate prefixes like `dbo:`, `dbr:`, and `rdf:`.
3. Construct a query that includes `SELECT`, `WHERE`, and any necessary `FILTER` or `ORDER BY` clauses.
4. If the question is ambiguous, create a query that returns broader results with a limit clause (e.g., `LIMIT 10`).

## Example:
User Query: "What is the capital of France?"
SPARQL Query:
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT ?capital WHERE {
  dbr:France dbo:capital ?capital .
}

Note: The SQL result should not have any special formatting like ``` or sparql at the beginning or ending.
    """
]

# Streamlit App Setup
#st.set_page_config(page_title="Spatial Mind", page_icon="🌍", layout="centered")
logo_path = "logo.jpg"  # Replace with your image file path or URL

# Sidebar with rounded logo using HTML/CSS


#st.sidebar.image('logo.jpg')

# Display the logo in the sidebar with CSS for rounding the edges
#st.sidebar.markdown('<img src="pic1.webp" class="sidebar-logo" width="150">', unsafe_allow_html=True)

# App Header
st.title("🌍 Spatial Mind")
st.subheader("Unlock the Power of Geospatial Data and SPARQL Queries")
st.markdown("---")

# Sidebar Info
st.sidebar.header("🔍 What is Spatial Mind?")
st.sidebar.info(
    """
    **Spatial Mind** uses Google Gemini to analyze geospatial data or convert English questions into SPARQL queries.
    
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
st.write("Enter your query below and get intelligent results.")
question = st.text_input("Type your question here:", key="input", placeholder="e.g., What is the capital of France?")

# Submit Button with custom style
submit = st.button("🔍 Get Answer", help="Click to process your query")

# Processing the Query
if submit:
    # SPARQL Query Section
    st.write("### 🧠 SPARQL Query")
    with st.spinner('🔍 Generating SPARQL query...'):
        response_sparql = get_gemini_prompt(question, S_prompt)
        st.code(response_sparql, language="sparql")

    # Geospatial Data Section
    st.markdown("---")
    st.write("### 📍 Geospatial Data Analysis")
    with st.spinner('🌍 Retrieving geospatial data...'):
        response_geo = get_gemini_prompt(question, prompt)
        st.success("Geospatial data retrieved successfully!")
        st.write(response_geo)

st.markdown(
    """
    ---
    <div style='text-align: center; font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; color: #4a4a4a;'>
        <p> <span style='font-style: italic;'>Rahshana K</span> & <span style='font-style: italic;'>Athirai</span> 🎓</p>
        
    </div>
    """, unsafe_allow_html=True
)
