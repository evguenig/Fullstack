import logging

import uvicorn

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

import schemas
import database


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get("/")
def get_root():
    return "Welcome to our API"


@app.get("/book/{book_id}")
async def retrieve_book(book_id: int):
    try:
        return await database.get_book(book_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=repr(e))


@app.post("/book/")
async def create_book(request: schemas.BookAuthorPayload):
    await database.add_book(convert_into_book_db_model(request.book), convert_into_author_db_model(request.author))
    return "New book added " + request.book.title + " " + str(request.book.number_of_pages) + " " \
        + " New author added " + request.author.first_name + " " + request.author.last_name


def convert_into_book_db_model(book: schemas.Book):
    return database.Book(title=book.title, number_of_pages=book.number_of_pages)


def convert_into_author_db_model(author: schemas.Author):
    return database.Author(first_name=author.first_name, last_name=author.last_name)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
