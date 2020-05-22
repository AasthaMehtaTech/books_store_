from app import db

class Course(db.Model):
    __tablename__ = 'course_tb'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email_address = db.Column(db.String())
    contact = db.Column(db.String())
    course_url = db.Column(db.String())
    english = db.Column(db.String())
    hindi = db.Column(db.String())

    def __init__(self,first_name,last_name,email_address,contact,course_url,english,hindi):
        self.first_name=first_name,
        self.last_name=last_name,
        self.email_address=email_address,
        self.contact=contact,
        self.course_url=course_url,
        self.english=english,
        self.hindi=hindi

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'first_name':self.first_name,
            'last_name': self.last_name,
            'email_address': self.email_address,
            'contact': self.contact,
            'course_url': self.course_url,
            'english': self.english,
            'hindi': self.hindi
        }
