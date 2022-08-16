# FastAPI Tutorial with Basic PyQuery Project
import os
import json
import random
import shutil
import string
import urllib.request
from fastapi import FastAPI, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse
from typing import  Union
from pyquery import PyQuery
from pydantic import BaseModel
from uuid import uuid4 # Universally Unique Identifier

# PyDantic BaseModel Class
class Item(BaseModel):
    name: str
    description: Union[str, None] = None # Optional value (See in FastAPI/docs)
    From: Union[str, None] = None
    MaxHeight: float # Optional value (See in FastAPI/docs)
    MaxWeight: float 
# Exception Class
class MyException(Exception):
    def __init__(self, name: str):
        self.name = name

Dokwiki_link = 'https://zh.m.wikipedia.org/zh-tw/%E7%8A%AC%E7%A8%AE%E5%88%97%E8%A1%A8'
doc = PyQuery(url=Dokwiki_link)
doc_tr = doc.find('tr').children()

# print(doc('td:nth-of-type(3)').text().split())
dog_name = doc.find('td:nth-of-type(2) a:nth-of-type(1)').text().split()
dog_name.remove('[1]')
dog_name.remove('[2]')
dog_name.remove('[3]')
# print(dog_name)
dog_type = doc.find('td:nth-of-type(4)').text().split(' ')
dog_from = doc.find('td:nth-of-type(5)').text().split(' ')

my_dog_type = dict(zip(dog_name, dog_type))
my_dog_from = dict(zip(dog_name, dog_from))

app = FastAPI() # FastAPI Module


wiki_dog = []
my_dog = 'dog.json'
my_dog_names = []
# Load local json file if exist
if os.path.exists(my_dog):
    with open(my_dog, "r") as f:
        wiki_dog = json.load(f)

@app.get('/show-dogname')
def show_dogname():
    return {'All dog name :' : dog_name}   

@app.get('/get-dog_from/{dog_id}')
def get_dogfrom(dog_id:str = '猴犬'):
    if dog_id not in dog_name:
        raise HTTPException(404, f"Dog name {dog_id} is not in your list")
    else:
        if dog_id in dog_name:
            return {f"Dog name = {dog_id}":f"Form = {my_dog_from[dog_id]}"}
        else:
            raise HTTPException(404, f"Dog name {dog_id} is not in your list")

@app.get('/get-dog_type/{dog_id}')
def get_dogtype(dog_id:int = 1):
    if dog_id not in dog_name:
        raise HTTPException(404, f"Dog name {dog_id} is not in your list")
    else:
        if dog_id in dog_name:
            return {f"Dog name = {dog_id}":f"type = {my_dog_type[dog_id]}"}
        else:
            raise HTTPException(404, f"Dog name {dog_id} is not in your list")

@app.exception_handler(MyException)
def call_exception_handler(request:Request, exc: MyException):
    return JSONResponse (
        status_code= 414,
        content= {
            'Message' : f'Oops ! {exc.name} did something. There goes a rainbow ...'
        }
    )
@app.post('/add-Newdog', response_model=Item)
def create_dog(item: Item):
    item_dict = item.dict()
    
    item_id = uuid4().hex
    item_dict.update({"id":item_id})
    wiki_dog.append(item_dict)
    # Save a new item into local database (JSON file)
    with open(my_dog, "w") as f:
        json.dump(wiki_dog, f, indent=4)
    return item_dict

@app.post('/upload')
def Upload_file(file: Union[UploadFile, None] = None):
    if not file: return {"message" : "No file upload"}
    try:
        file_location = './' + file.filename
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
            file.close()
        my_dog_names.append(file.filename)
        return {"Result" : "OK"}
    except:
        raise MyException(name=f'Upload File {file.filename}')