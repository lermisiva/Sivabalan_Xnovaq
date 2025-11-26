# uvicorn main:app --reload
from fastapi import FastAPI , HTTPException

app =  FastAPI(title = "MyBookAPI")

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    # {"id": 4, "title":"moby"}
]
@app.get("/books") 
def get_books():
    return {"books": books}