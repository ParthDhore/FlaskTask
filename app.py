from flask import Flask, Response, request,jsonify, make_response, json
from flask_mongoengine import MongoEngine
from decouple import config

app=Flask(__name__)

database_name="bookinfo"
password=config("mongo_password")
DB_URI="mongodb+srv://admin:{}@flaskapp.mdlfoa8.mongodb.net/{}?retryWrites=true&w=majority".format(password,database_name)

db=MongoEngine()
db.connect(db=database_name,username='admin',password=password,host=DB_URI)

class Book(db.Document):
    book_id= db.IntField()
    name= db.StringField()
    author= db.StringField()

    def to_json(self):
        return {
            "book_id": self.book_id,
            "name": self.name,
            "author": self.author
        }


@app.route('/books/createBook',methods=['POST'])
def api_create():
    if request.method=="POST":
        content=request.json
        book=Book(book_id=content['book_id'],name=content['name'],author=content['author'])
        book.save()
        return make_response("Book Added",201)


@app.route('/books',methods=['GET'])
def api_books():
    if request.method=="GET":
        books=[]
        for book in Book.objects:
            books.append(book.to_json())
        print(books)
        return make_response(jsonify(books),200)

    

@app.route('/books/<book_id>',methods=['GET','PUT','DELETE'])
def db_api_book(book_id):
    if request.method=="GET":
        book_obj=Book.objects(book_id=book_id).first()
        if book_obj:
            return make_response(jsonify(book_obj.to_json()),200)
        
        else:
            return make_response("No Book with that ID",404)

    elif request.method=="PUT":
        content=request.json
        book_obj=Book.objects(book_id=book_id).first()
        book_obj.update(name=content['name'],author=content['author'])
        return make_response("",204)
    
    elif request.method=="DELETE":
        content=request.json
        book_obj=Book.objects(book_id=book_id).first()
        book_obj.delete()
        return make_response("",204)


if __name__=="__main__":
    app.run(debug=True)