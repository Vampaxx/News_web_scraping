# FastAPI Web Scraper Application

This FastAPI application allows you to process a given URL, extract important details through web scraping, and save the resulting JSON data into a MySQL database. Additionally, it allows you to retrieve the stored data by its ID.

## Features

- **POST /url/**: Submits a URL for processing, scrapes content, and saves the extracted data in a MySQL database.
- **GET /data/{id}**: Retrieves the stored data by its unique ID.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.9+
- MySQL Server
- fastapi  
- SQLAlchemy
- requests  
- uvicorn                 
- Langchain

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Vampaxx/News_web_scraping
    cd News_web_scraping
    ```

2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Add your API key into .env:**
    ```bash
    db_host      = your_mysql_host      
    db_user      = your_mysql_username  
    db_password  = your_mysql_password  
    db_name      = your_database_name      
    
5. **Configure MySQL:**
Ensure your MySQL server is running, and create the necessary database and table:
    ```bash
    CREATE DATABASE News_database;
    
    USE News_database;
    
    CREATE TABLE web_scraper (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Important_details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
  6. **Running the Application**

    ```bash
    python app.py
## Usage

1. **Start the FastAPI server:**
    ```bash
    uvicorn app:app --reload
    ```

2. **POST /url/**: Submit a URL for processing.
    - Example request:
      ```bash
      curl -X POST "http://127.0.0.1:8000/url/" -H "Content-Type: application/json" -d '{"URL": "https://example.com"}'
      ```
    - Example response:
      ```json
      {
          "id": 1,
          "details": { "title": "Sample Title", "content": "Sample Content" }
      }
      ```

3. **GET /data/{id}**: Retrieve the scraped data by its ID.
    - Example request:
      ```bash
      curl -X GET "http://127.0.0.1:8000/data/1"
      ```
    - Example response:
      ```json
      {
          "id": 1,
          "details": { "title": "Sample Title", "content": "Sample Content" }
      }
      ```

## Project Structure

```plaintext
├── app
│   ├── app.py           # FastAPI application
│   ├── models.py         # SQLAlchemy models
│   
├── requirements.txt      # List of dependencies
├── README.md             # Project documentation
└── .env                  # Environment variables for DB connection and API keys
