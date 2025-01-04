# GeoM: Geospatial Data Retrieval System with LLM

## Overview
The Geospatial Data Retrieval System is a powerful solution for querying and analyzing geospatial data from both local and open-source databases.
It utilises an LLM (Gemini Pro) to process natural language queries and dynamically generates SQL or SPARQL queries to retrieve the desired data.




## Features
- **Dual Query Modules**:  
  - **Local Database Querying**: Retrieves geospatial data from a PostGIS database using SQL queries.  
  - **Open-Source Database Querying**: Fetches data from sources like Wikidata and DBpedia using SPARQL queries.  

- **Intelligent Query Processor**: Natural language queries are processed by an LLM that utilizes predefined handbooks for context.  

- **Error Handling**: Incorporates basic validation and error-checking mechanisms for generated queries.  

## Technologies Used

### Programming Language
- Python

### Database
- PostgreSQL with **PostGIS** extension
- DBpedia
- Wikidata

### Large Language Model (LLM)
-  Gemini Pro

### Libraries
- **psycopg2**: For connecting to the PostgreSQL database.
- **requests**: For making API calls to open-source databases like Wikidata and DBpedia.
- **geojson**: For handling geospatial data formats.
- **Streamlit**: For Deployment


## System Architecture

![unnamed (5)](https://github.com/user-attachments/assets/ed5004c0-00f2-4ae1-b2a9-2f95f6cec62e)

## **Core Components**  
- **LLM Query Processor Module**:
  - Handles natural language queries using predefined handbooks for local and open-source data sources.
  - Converts user queries into context-aware SQL or SPARQL queries.
  
- **Query Generation Module**:
  - **SQL Query Generation**: For PostGIS database queries.
  - **SPARQL Query Generation**: For querying Wikidata and DBpedia.

- **Data Fetching Module**:
  - Executes SQL queries via Python (psycopg2) for the local PostGIS database.
  - Executes SPARQL queries using APIs for open-source databases.
 
## Output:

### Retrieval from Local database:

![unnamed](https://github.com/user-attachments/assets/d2aaa4e4-33c7-4331-a06e-c31dcdb5b868)

---
![unnamed (1)](https://github.com/user-attachments/assets/d193435b-8663-4eb2-9d05-5e62350167ac)

---

### Retrieval from open database:

![unnamed (2)](https://github.com/user-attachments/assets/1bc5c253-6767-4af9-9e32-8f896ad2d007)

---
![unnamed (3)](https://github.com/user-attachments/assets/b2678646-5a8d-4e44-9b43-7f0f6d85df8b)

---

### Newyork Database:
![unnamed (4)](https://github.com/user-attachments/assets/e06fc1be-d7e7-4b32-a839-36c8e3f0ad71)

### Note: 
- This project not only works for the mentioned Newyork database but also works good for any kind of local database.
- Ensure to change the prompt(handbook) according to your database.









---
