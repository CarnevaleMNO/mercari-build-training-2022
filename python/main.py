import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import db
import hashlib

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [os.environ.get('FRONT_URL', 'http://localhost:3000')]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# GET root


@app.get("/")
def root():
    return {"message": "Hello, world!"}

# GET /items


@app.get("/items")
def read_items():
    return db.show_items()

# GET /items/{id}


@app.get("/items/{id}")
def read_item(id: int):
    item = db.get_item(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# GET /search?keyword=keyword


@app.get("/search")
def search_items(keyword: Optional[str] = None):
    if keyword is None:
        raise HTTPException(status_code=400, detail="keyword is required")
    return db.search_items(keyword)

# POST /items and save to /images


@app.post("/items")
def add_item(name: str = Form(...), category_id: int = Form(...), image: str = Form(...)):
    image_hash = hash_image(image)
    db.create_item(name, category_id, image_hash)
    return {"message": "Item created"}
    
    # return db.create_item(name, category_id, image)

@app.get("/image/{items_image}")
async def get_image(items_image):
    # Create image path
    image = images / items_image
    if not items_image.endswith(".jpg"):
        raise HTTPException(
            status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.info(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)

# PUT /items/{id}
@app.put("/items/{id}")
def update_item(id: int, name: str = Form(...), category_id: int = Form(...), image: str = Form(...)):
    db.update_item(id, name, category_id, image)
    return {"message": "Item updated"}

# Delete /items/{id}
@app.delete("/items/{id}")
def delete_item(id: int):
    item = db.get_item(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete_item(id)
    return {"message": "item deleted"}


# hash image with sha256 and save in /images as jpg
def hash_image(image):  
    filename = ""
    filename = filename + image
    readable_hash = ""
    # filename = "images/test.jpg"
    with open(filename, "rb") as f:
        bytes = f.read()
        readable_hash = readable_hash + hashlib.sha256(bytes).hexdigest()
        # print(readable_hash + ".jpg") 
    with open("images/" + readable_hash + ".jpg", "wb") as f:
        f.write(bytes)
    return readable_hash