from dotenv import load_dotenv
from functools import lru_cache
import os
import pathlib
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from .airtable import Airtable
BASE_DIR = pathlib.Path(__file__).parent # src

app = FastAPI()
templates = Jinja2Templates(directory = BASE_DIR / "templates" )


@lru_cache()
def cached_dotenv():
    load_dotenv()

cached_dotenv()

AIRTABLE_BASE_ID = 'appJkV4EPn9X46PUb'
AIRTABLE_API_KEY = 'keykY5YjFxN23izT6'
AIRTABLE_TABLE_NAME = 'fastapi-to-airtable'



@app.get("/")
def home_view(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/")
def home_signup_view(request: Request, email:str = Form(...)):
    """
    TODO add CSRF for security
    """

    # Envio de emaail a airtable
    airtable_client =  Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
        table_name=AIRTABLE_TABLE_NAME,
    )
   
    did_send = airtable_client.create_records({"email": email})
    return templates.TemplateResponse("home.html", {"request": request, "submitted_email": email, "did_send": did_send})