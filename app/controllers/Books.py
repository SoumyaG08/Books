"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Books(Controller):
    def __init__(self, action):
        super(Books, self).__init__(action)
        """
        This is an example of loading a model.
        Every controller has access to the load_model method.
        """
        self.load_model('User')
        self.load_model('Book')
        self.db = self._app.db

        """
        
        This is an example of a controller method that will load a view for the client 

        """
   
    def index(self):
        """
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_users()
        
        self.models['WelcomeModel'].add_message()
        # messages = self.models['WelcomeModel'].grab_messages()
        # user = self.models['WelcomeModel'].get_user()
        # to pass information on to a view it's the same as it was with Flask
        
        # return self.load_view('index.html', messages=messages, user=user)
        """
        return self.load_view('index.html')

    def home(self):
        blist = self.models['Book'].get_3reviews()
        rbooks = self.models['Book'].get_reviewed_books()
        return self.load_view('home.html',reviews=blist,books=rbooks)

    def books_add(self):
        return self.load_view('add.html')

    def add_process(self):
        print "form: ", request.form
        print "request.form['author_w']:", request.form['author_w']
        print "request.form['author_d']:", request.form['author_d']
        if request.form['author_w']:
            author = request.form['author_w']
        else:
            author = request.form['author_d']
        print "author: ", author
        review_details = {
            'title': request.form['title'],
            'author': author,
            'review': request.form['review'],
            'rating': int(request.form['rating']),
            'user_id': int(session['id'])
        }
        books = self.models['Book'].add_book(review_details)
        url = '/books/' + str(books['id'])
        return redirect(url)

    def show(self, id):
        book = self.models['Book'].get_book_by_id(id)
        review = self.models['Book'].get_book_reviews(id)
        print "book[0]", book[0]
        return self.load_view('bookDetails.html',book=book[0], reviews=review)

