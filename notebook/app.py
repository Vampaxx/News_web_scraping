import os 
import json
#import mysql.connector
import pymysql

from dotenv import load_dotenv
from urllib.parse import urlparse
from fastapi import FastAPI,HTTPException

from News_web_scraping import logger 
from News_web_scraping.pipeline.stage_04_combining import CombiningPipeline


app = FastAPI()


load_dotenv()
db_host     = os.getenv("db_host")
db_user     = os.getenv("db_user")
db_password = os.getenv("db_password")
db_name     = os.getenv("db_name")
response = {
  "Galaxy A16 Models": {
    "A16 5G": {
      "Chipset": "Samsung Exynos 1330 (Europe) / MediaTek Dimensity 6300 (other regions)",
      "Display": "6.7-inch Super AMOLED (FHD+ 90Hz)",
      "Camera": "50MP main cam, 5MP ultrawide, 2MP macro",
      "Battery": "5,000 mAh with 25W charging",
      "RAM": "4GB",
      "Storage": "128GB (expandable via microSD)",
      "Android Updates": "Up to 6 years",
      "Price": "€240 (Europe)"
    },
    "A16 4G": {
      "Chipset": "MediaTek Helio G99",
      "Display": "6.7-inch Super AMOLED (FHD+ 90Hz)",
      "Camera": "50MP main cam, 5MP ultrawide, 2MP macro",
      "Battery": "5,000 mAh with 25W charging",
      "RAM": "4GB",
      "Storage": "128GB (expandable via microSD)",
      "Android Updates": "Up to 6 years",
      "Price": "€210 (Europe)"
    }
  }
}


def get_db_connection():
    try:
        connection = pymysql.connect(host   = db_host,                                   
                                    user    = db_user,
                                    password= db_password,
                                    database= db_name,
                                    #cursorclass=pymysql.cursors.DictCursor
                                )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")




@app.get("/get_data/{URL:path}")
async def get_data(URL: str):

    # Validate the URL
    parsed_url = urlparse(URL)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    # Simulate processing the URL (replace with actual processing logic)
    response = {
        "url": "1",
        "status": "processed",
        "data": {"key1": "value1", "key2": 2}
    }

    # Ensure the response is a dictionary
    if not isinstance(response, dict):
        raise HTTPException(status_code=500, detail="Response is not in expected dictionary format")

    # Convert response to JSON string
    json_response = json.dumps(response)


    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM News_table"
            cursor.execute(sql)
            items = cursor.fetchall()

        return {"items": items} 
    except:
        return f"{json_response},{items}" 

    
    """# Save the JSON response to MySQL
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO News_table (Important_details) VALUES (%s)"
            cursor.execute(sql, (json_response,))
            connection.commit()  # Commit the transaction
    except Exception as e:
        print(f"Error while inserting data: {e}")  # Log the error
        raise HTTPException(status_code=500, detail="Data insertion failed")
    finally:
        if connection:
            connection.close()  # Ensure the connection is closed"""

    #return {"message": "Data saved successfully", "data": json_response}






@app.post("/get_data/{URL:path}")
async def get_data__(URL: str):

    parsed_url = urlparse(URL)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    #pipeline        = CombiningPipeline(URL=URL)
    #response        = pipeline.main()
    

    if not isinstance(response, dict):
        raise HTTPException(status_code=500, detail="Response is not in expected dictionary format")

    json_response   = json.dumps(response)
    connection      = None

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO News_table (Important_details) VALUES (%s)"
            cursor.execute(sql, (json_response,))
            connection.commit()  # Commit the transaction
    except Exception as e:
        logger.info(f"Error while inserting data: {e}")
        print(f"Error while inserting data: {e}")
        raise HTTPException(status_code=500, detail="Data insertion failed")
    finally:
        if connection:
            connection.close()  # Ensure the connection is closed

    return {"message": "Data saved successfully", "data": response}
    #return f"{response}== {type(response)}"

    

    