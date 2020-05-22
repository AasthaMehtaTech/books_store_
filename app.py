import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Course

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/add")
def add_book():
    name=request.args.get('name')
    author=request.args.get('author')
    published=request.args.get('published')
    try:
        book=Book(
            name=name,
            author=author,
            published=published
        )
        db.session.add(book)
        db.session.commit()
        return "Book added. book id={}".format(book.id)
    except Exception as e:
	    return(str(e))

@app.route("/getall")
def get_all():
    try:
        books=Book.query.all()
        return  jsonify([e.serialize() for e in books])
    except Exception as e:
	    return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book=Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/add_course/",methods=['GET', 'POST'])
def add_course_form():
    if request.method == 'POST':
        first_name=request.form.get('first_name')
        last_name=request.form.get('last_name')
        email_address=request.form.get('email_address')
        contact=request.form.get('contact')
        course_url=request.form.get('course_url')
        english=request.form.get('english')
        hindi=request.form.get('hindi')
        try:
            course=Course(
                first_name=first_name,
                last_name=last_name,
                email_address=email_address,
                contact=contact,
                course_url=course_url,
                english=english,
                hindi=hindi
            )
            db.session.add(course)
            db.session.commit()
            return "Course added. course id={}".format(course.id)
        except Exception as e:
            return(str(e))
    return render_template("add_course.html")

@app.route("/search_buddy/",methods=['GET', 'POST'])
def search_buddy_form():
    if request.method == 'POST':
        course_url=request.form.get('course_url')
        english=request.form.get('english')
        hindi=request.form.get('hindi')
        try:
            course=Course.query.filter_by(course_url=course_url).filter(or_(Course.english == english, Course.hindi == hindi)).first()
            return jsonify(course.serialize())
        except Exception as e:
    	    return(str(e))
    return render_template("search_buddy.html")

if __name__ == '__main__':
    app.run()
