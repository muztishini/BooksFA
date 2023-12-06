from fastapi import FastAPI, Depends, Body, status
from database import *
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/api/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.get('/api/books/{id}', status_code=status.HTTP_200_OK)
async def get_book(id, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first()
    if book == None:
        return JSONResponse(status_code=404, content={"message": "Книга не найдена"})
    else:
        return book


@app.post('/api/books', status_code=status.HTTP_201_CREATED)
async def add_book(data=Body(), db: Session = Depends(get_db)):
    book = Book(name=data['name'], author=data['author'],
                year=data['year'], isbn=data['isbn'])
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.put("/api/books/{id}", status_code=status.HTTP_201_CREATED)
async def edit_book(id, data=Body(), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first()
    if book == None:
        return JSONResponse(status_code=404, content={"message": "Книга не найдена"})
    book.name = data['name']
    book.author = data['author']
    book.year = data['year']
    book.isbn = data['isbn']
    db.commit()
    db.refresh(book)
    return book


@app.delete('/api/books/{id}')
async def get_book(id, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first()
    if book == None:
        return JSONResponse(status_code=404, content={"message": "Книга не найдена"})
    db.delete(book)
    db.commit()
    return book
