from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, select
from sqlalchemy.orm import registry, relationship, Session

engine = create_engine("mysql+mysqlconnector://test:test@localhost:3306/books", echo=True)

mapper_registry =  registry()                          
Base = mapper_registry.generate_base()


class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    
    
    def __repr__(self):
        return f"""
        <Author(id={self.id}, first_name={self.first_name}, 
            last_name={self.last_name})>
            """

# Define books table
class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True)
    title = Column(String(length=255), nullable=False)
    number_of_pages = Column(Integer)

    def __repr__(self):
        return f"<Book(book_id={self.book_id}, title={self.title}, num_of_pages={self.number_of_pages})"

class BookAuthor(Base):
    __tablename__ = 'bookauthors'

    bookauthor_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.author_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))

    author = relationship("Author")
    book = relationship("Book")

    def __repr__(self):
        return f"""
            <BookAuthor(bookauthor_id={self.book_id}, 
            author_id={self.author_id}, book_id={self.book_id},
            first_name={self.author.first_name}, last_name={self.author.last_name},
            title={self.book.title})>
            """


# Create all tables
Base.metadata.create_all(engine)


def add_book(book: Book, author: Author):
    with Session(engine) as session:
        existing_book = session.execute(
            select(Book).filter(Book.title == book.title, Book.number_of_pages == book.number_of_pages)).scalar()
        if existing_book is not None:
            print("The book has already been added")
            return
        print("Adding Book")
        session.add(book)

        existing_author = session.execute(
            select(Author).filter(Author.first_name == author.first_name, Author.last_name == author.last_name)).scalar()
        if existing_author is not None:
            print("Author has already been added")
            session.flush()
            pairing = BookAuthor(author_id=existing_author.author_id, book_id=book.book_id)
        else:
            print("Adding Author")
            session.add(author)
            session.flush()
            pairing = BookAuthor(author_id=author.author_id, book_id=book.book_id)

        session.add(pairing)
        session.commit()
        print("New pairing added " + str(pairing))


def get_book(book_id: int):
    with Session(engine) as session:
        book = session.execute(select(Book).filter(Book.book_id == book_id)).scalar()
        if book is None:
            raise Exception('Book does not exist')
        pairing = session.execute(select(BookAuthor).filter(BookAuthor.book_id == book_id)).scalar()
        author = session.execute(select(Author).filter(Author.author_id == pairing.author_id)).scalar()
        return book, author

