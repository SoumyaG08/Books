""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class Book(Model):
    def __init__(self):
        super(Book, self).__init__()

    def get_3reviews(self):
        return self.db.query_db("SELECT books.title as title,reviews.rating as rating,users.alias as alias,reviews.review as reviews,DATE_FORMAT(reviews.created_at,'%M %d, %Y') as date,books.id as booksid, users.id as usersid FROM books JOIN reviews ON books.id = reviews.book_id LEFT JOIN users ON reviews.user_id = users.id order by reviews.id desc limit 3")

    def get_reviewed_books(self):
        return self.db.query_db("SELECT books.id as bookid, books.title as title FROM books JOIN reviews ON reviews.book_id = books.id group by title")

    def add_book(self, review):
        bquery = 'SELECT * FROM books WHERE title = :title'
        data = { 'title': review['title']}
        book = self.db.query_db(bquery, data)

        if book:
            #Insert into reviews table only
            query = "INSERT INTO reviews (review, rating, user_id, book_id, created_at) VALUES (:review, :rating, :user_id, :book_id, NOW())"
            data = {'review': review['review'], 'rating': int(review['rating']), 'user_id': int(review['user_id']), 'book_id':int(book[0]['id'])}
            self.db.query_db(query, data)
            # return {'book':book[0]}
            return book[0]
        else:
            #Insert into reviews and books
            query1 = "INSERT INTO books (title, author, created_at) VALUES (:title, :author, NOW())"
            data1 = {'title': review['title'], 'author': review['author']}
            self.db.query_db(query1, data1)
            #Fetch the last inserted book
            bdata = self.db.query_db("SELECT * FROM books ORDER BY id desc limit 1")
            #Insert the review for the book in the review table
            query2 = "INSERT INTO reviews (review, rating, user_id, book_id, created_at) VALUES (:review, :rating, :user_id, :book_id, NOW())"
            data2 = {'review': review['review'], 'rating': int(review['rating']), 'user_id': int(review['user_id']), 'book_id': int(bdata[0]['id'])}
            self.db.query_db(query2, data2)
            # return{'book':bdata[0]}
            return bdata[0]

    def get_book_by_id(self, id):
        query = "SELECT * FROM books WHERE id = :id"
        data = { 'id': id}
        return self.db.query_db(query, data)

    def get_book_reviews(self, id):
        query = "SELECT reviews.rating as rating,reviews.review as reviews,DATE_FORMAT(reviews.created_at,'%M %d, %Y') as date,books.id as booksid, users.id as usersid, users.alias as alias FROM books JOIN reviews ON books.id = reviews.book_id LEFT JOIN users ON reviews.user_id = users.id WHERE books.id = :id"
        data = {'id': id}
        return self.db.query_db(query, data)
        
        
    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """