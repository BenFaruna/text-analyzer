from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime

import pymongo
from flask import Flask, Response, redirect, render_template, request, url_for

from alphabets import Alphabets


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

MONGODB_URL = 'mongodb+srv://neobot:neodynamics@30daysofpython-pa4u3.mongodb.net/<dbname>?retryWrites=true&w=majority'

client = pymongo.MongoClient(MONGODB_URL)

db = client['thirty_days_of_python']


@app.route('/')
def home():
    techs = ['HTML', 'CSS', 'Python', 'Flask',  'MongoDB']
    name = '30 Days of Python Programming'
    return render_template('home.html', techs=techs, name = name, title= 'Home')


@app.route('/about')
def about():
    name = 'Coding For all'
    return render_template('about.html', name=name, title='About Us')


@app.route('/post', methods=['GET', 'POST'])
def post():
    name = 'Text Analyzer'
    if request.method == 'POST':
        return redirect({{url_for('result')}})
    else:
        return render_template('post.html', name=name, title=name)


@app.route('/result.html', methods=['GET', 'POST'])
def result():
    name = 'Text Analysis Result'
    if request.method == 'POST':
        content = request.form['content']
        result = Alphabets(content)
        total_words, num_of_char, most_frequent_word, words, word_num = result.num_of_words(), result.num_of_chars(), result.most_frequent()[0], result.identify(), result.count().items()

        return render_template('result.html', name=name, title='Result', word_count=total_words, char_num=num_of_char, 
        frequent=most_frequent_word, words=words, word_num=word_num)


@app.route('/api/v1.0/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        
        return redirect(url_for('student_list'))
    else:
        
        student = db.students.find()
        return Response(dumps(student), mimetype='application/json')


@app.route('/api/v1.0/students/<id>', methods=['GET', 'POST'])
def find_students(id):
    if request.method == 'POST':
        delete_student(id)
        return redirect(url_for('student_list'))

    else:

        student = db.students.find_one({'_id' : ObjectId(id)})

        return Response(dumps(student), mimetype='application/json')


@app.route('/students/', methods=['GET', 'POST'])
def student_list():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['birthyear']
        country = request.form['country']
        city = request.form['city']
        skills = request.form['skills'].split(', ')
        bio = request.form['bio']
        created_on = datetime.now()

        student = {
            'name' : name,
            'country': country,
            'city': city,
            'birthyear': dob,
            'skills': skills,
            'bio': bio,
            'created_at': created_on
        }
        db.students.insert_one(student)
        return redirect(url_for('student_list'))
    else:
        students_list = db.students.find()

        return render_template('students/students.html', students=students_list)


@app.route('/students/add/', methods=['GET', 'POST'])
def create_student():

        return render_template('students/add.html')


@app.route('/students/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        update_student(id)
        return redirect(url_for('student_list'))

    else:
        query = {'_id':ObjectId(id)}
        student = db.students.find_one(query)

        return render_template('students/update/update_id.html', student=student)


@app.route('/api/v1.0/students/update/<id>', methods=['PUT'])
def update_student(id):
    query = {'_id':ObjectId(id)}

    name = request.form['name']
    dob = request.form['birthyear']
    country = request.form['country']
    city = request.form['city']
    skills = request.form['skills'].split(', ')
    bio = request.form['bio']
    created_on = datetime.utcnow()

    student = [
        {'$set': {'name' : name}},
        {'$set': {'country': country}},
        {'$set': {'city': city}},
        {'$set': {'birthyear': dob}},
        {'$set': {'skills': skills}},
        {'$set': {'bio': bio}},
        {'$set': {'created_at': created_on}}
    ]

    db.students.update_one(query, student)

    return


@app.route('/api/v1.0/students/update/<id>', methods=['GET', 'POST'])
def update_help(id):
    if request.method == 'POST':
        update_student(id)
        return redirect(url_for('student_list'))

    else:
        return redirect(url_for('students'))


@app.route('/api/v1.0/student/<id>', methods=['DELETE'])
def delete_student(id):
    
    query = {'_id':ObjectId(id)}

    db.students.delete_one(query)

    return


if __name__ == '__main__':
    app.run(debug=True)
