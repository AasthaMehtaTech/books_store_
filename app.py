import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Course

def url_cleaner(course_url):
    ignore_char = ['https', 'www', '.in', 'http', '.com', ':', '//']  # Replaced with Nothing
    unwanted_char = ['/', '?', '.', '=', '-', '+']  # Replaced with Single Space
    clean_url = course_url
    for char in ignore_char:
        clean_url = clean_url.replace(char, '')
    for char in unwanted_char:
        clean_url = clean_url.replace(char, ', ')
    return clean_url

def most_common(ini_list, len = 10):
    result = sorted(set(ini_list), key = ini_list.count, reverse = True)
    return result[:len]

@app.route("/")
def index():
    return render_template("index.html")

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
        clean_url = url_cleaner(course_url)
        course_tags = clean_url.lower()
        try:
            course=Course(
                first_name=first_name,
                last_name=last_name,
                email_address=email_address,
                contact=contact,
                course_url=course_url,
                english=english,
                hindi=hindi,
                course_tags=course_tags
            )
            db.session.add(course)
            db.session.commit()
            return "Course added. course id={}".format(course.id)
        except Exception as e:
            return(str(e))
    return render_template("add_course.html")

@app.route("/search_buddy/",methods=['GET', 'POST'])
def search_buddy_form():
    students_detail = list()
    result_description = ''
    if request.method == 'POST':
        course_url=request.form.get('course_url')
        english=request.form.get('english')
        hindi=request.form.get('hindi')
        try:
            course=Course.query.filter_by(course_url=course_url).filter(or_(Course.english == english, Course.hindi == hindi)).all()
            for item in course:
                data = item.serialize()
                languages = ''
                if data['english']=='on' and data['hindi']=='on':
                    languages += 'English, Hindi'
                elif data['english']=='on':
                    languages += 'English'
                elif data['hindi']=='on':
                    languages += 'Hindi'
                data['languages'] = languages
                students_detail.append(data) # jsonify(course.serialize())
            result_description = f'Results for {course_url}:'
            return render_template("search_buddy.html", students_detail=students_detail, result_description=result_description)
        except Exception as e:
    	    return(str(e))
    return render_template("search_buddy.html", students_detail = students_detail, result_description=result_description)

@app.route("/search_course/",methods=['GET', 'POST'])
def search_course_form():
    courses_detail = list()
    result_description = ''
    if request.method == 'POST':
        course_tags=request.form.get('course_tags')
        course_tags_list = course_tags.lower().split(',')
        try:
            course_list = list()
            for tag in course_tags_list:
                courses=Course.query.filter(Course.course_tags.like(f'%{tag}%')).with_entities(Course.course_url).all()
                url_list = list(set([url[0] for url in courses]))
                course_list.extend(url_list)
            results = most_common(course_list)
            courses_detail.extend(results) # jsonify(course.serialize())
            result_description = f'Results for {course_tags}:'
            return render_template("search_course.html", courses_detail=courses_detail, result_description=result_description)
        except Exception as e:
    	    return(str(e))
    return render_template("search_course.html", courses_detail = courses_detail, result_description=result_description)

# TODO:
# Implement Find Learners   [YES]
# Homepage                  [YES]
# Deploy on Heroku          []

if __name__ == '__main__':
    app.run()
