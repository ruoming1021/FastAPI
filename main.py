'''
Python Packages Install
    > pip install -r requirements.txt
How to run
    > uvicorn main:app --reload
'''
# FastAPI Tutorial with Basic PyQuery Project
import os
import json
import random
import shutil
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
    price: float
    tax: Union[float, None] = None # Optional value (See in FastAPI/docs)

# Exception Class
class MyException(Exception):
    def __init__(self, name: str):
        self.name = name

# Pokedex Link
pokemons_link = 'https://zh.m.wikipedia.org/zh-tw/%E7%8A%AC%E7%A8%AE%E5%88%97%E8%A1%A8'

# Get all information from link (html)
doc = PyQuery(url=pokemons_link)
# Get information under <tr>
pokemons_ = doc.find('tr').children()
# Find out all text value in class 'infocard-cell-data' and split as a list
pokemons_index = pokemons_.find('.infocard-cell-data').text().split(' ')
# Find out all text value in class 'ent-name' and split as a list
pokemons_name = pokemons_.find('.ent-name').text().split(' ')
# Create a dictionary with keys and values
my_pokedex = dict(zip(pokemons_index, pokemons_name))

app = FastAPI() # FastAPI Module

# Local data initialize
my_items = []
my_file = 'item.json'
my_file_names = []
# Load local json file if exist
if os.path.exists(my_file):
    with open(my_file, "r") as f:
        my_items = json.load(f)

'''
Wrong Example (API Definition Order)
You should define the special path on top !
See <----

@app.get('/books/{book_id}') <----
def get_book(book_id: string):
    print(f'Return book to Client: {book_id}')
    return book_id
@app.get('/books/only_for_me') <----
def get_book_only_for_me(book_id: string):
    return 'the book that I can read only'
'''
# GET Method Exercise (Basic)
@app.get('/')
def root():
    return {"message": "Hello Welcome to  My FastAPI in Web writing by Python"}

# GET Method Exercise
@app.get('/random-pokemon')
def random_pokemon():
    return random.choice(list(my_pokedex.items()))

'''
    ---> Try to Change this API below into path parameter API ! <---
    Where is their difference ? You can see page 17 in powerpoint !
'''
# GET Method Exercise (Interact with local database), query parameter
@app.get('/get-pokemon/{poke_id}') #get-pokemon/10
def get_pokemon(poke_id: int = 1):
    if poke_id > len(my_pokedex):
        '''
            ---> Try to Change this HTTPException below into your own Exception ! <---
            You can use any status_code between 400 to 499 as client error
        '''
        raise HTTPException(404, f"Pokemon ID {poke_id} is not in your pokedex")
    else:
        # Turn integer value to string and leading zero as len == 3
        pokemon_id = str(poke_id).zfill(3)
        # Find out if pokemon_id is in database
        if pokemon_id in my_pokedex:
            return {f"Pokemon ID = {pokemon_id}":f"Pokemon Name = {my_pokedex[pokemon_id]}"}
        else:
            raise HTTPException(404, f"Pokemon ID {pokemon_id} is not in your pokedex")

# GET Method Exercise
@app.get('/show-pokemons')
def show_pokemons():
    return {'This is my pokedex' : my_pokedex}

# Exception Handler
@app.exception_handler(MyException)
def call_exception_handler(request:Request, exc: MyException):
    return JSONResponse (
        status_code= 420,
        content= {
            'Message' : f'Oops ! {exc.name} did something. There goes a rainbow ...'
        }
    )

# POST Method Exercise
@app.post('/add-item', response_model=Item)
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax":price_with_tax})
    # Generate an UUID with HEX code
    item_id = uuid4().hex
    item_dict.update({"id":item_id})
    my_items.append(item_dict)
    # Save a new item into local database (JSON file)
    with open(my_file, "w") as f:
        json.dump(my_items, f, indent=4)
    return item_dict

# GET/POST Method Result
@app.get('/show-items')
def show_item():
    if len(my_items):
        return {'Items':my_items}
    else:
        # Create a exception message
        raise HTTPException(404, 'Item not found')

'''
Inorder to recieve upload file
You need to install a new package
>   pip install python-multipart
Because FastAPI didn't have build-in file.save function,
    you need to import another module to help you save file.
>   import shutil
'''
# POST Method Exercise (Upload File & Save to local)
@app.post('/upload')
def Upload_file(file: Union[UploadFile, None] = None):
    if not file: return {"message" : "No file upload"}
    try:
        file_location = './' + file.filename
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
            file.close()
        my_file_names.append(file.filename)
        return {"Result" : "OK"}
    except:
        raise MyException(name=f'Upload File {file.filename}')

'''
Notion:
    If you want to run this command below
        > python main.py
    You have to uncomment the main function below !
'''
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app= 'main:app', reload= True) # Default host = 127.0.0.1, port = 8000