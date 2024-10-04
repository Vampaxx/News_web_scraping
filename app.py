import os 
import json 
import models
from pathlib import Path
from typing import Annotated
from pydantic import BaseModel,HttpUrl

from sqlalchemy.orm import Session
from urllib.parse import urlparse
from database import engine,SessionLocal
from fastapi.responses import JSONResponse
from fastapi import FastAPI,HTTPException,Depends,status


from News_web_scraping import logger 
from News_web_scraping.pipeline.stage_04_combining import CombiningPipeline


app = FastAPI()
models.Base.metadata.create_all(engine)



@app.post("/url/", )
async def create_table(URL: str):
    try:
        db          = SessionLocal()
        pipeline    = CombiningPipeline(URL=URL)  # Pass the URL directly as a string
        response    = pipeline.main()
        if not isinstance(response, dict):
            raise HTTPException(status_code=500, detail="Invalid response format, expected JSON.")
        db_table = models.NewsTable(Important_details=response)
        db.add(db_table)
        db.commit()
        db.refresh(db_table)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": db_table.id, "details": response})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@app.get("/data/{id}", status_code=status.HTTP_200_OK)
async def get_data(id: int):
    try:
        db          = SessionLocal()
        db_table    = db.query(models.NewsTable).filter(models.NewsTable.id == id).first()

        
        if db_table is None:
            raise HTTPException(status_code=404, detail=f"Data with id {id} not found.")

        
        return JSONResponse(status_code=status.HTTP_200_OK, content={"id": db_table.id, "details": db_table.Important_details})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))






