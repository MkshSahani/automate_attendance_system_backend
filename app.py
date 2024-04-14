from flask import Flask, request, flash, jsonify
from werkzeug.utils import secure_filename
from services.attdance_system import *
from startup import *
import json

app = Flask(__name__)

@app.route('/register', methods = ['POST'])
def register_new_user():
    body = request.data
    userDetails = json.loads(body)
    existringUser = list(db.users.find(
        {
            "$or": 
            [ 
                {"username": userDetails['username']},
                {"email":  userDetails["email"]}
            ]
        }
    ))
    print(existringUser)
    if(len(existringUser) > 0):
        return {
            'status_code': 400,
            'message': "username or email address adready exists.",
            'data': {}
        }

    db.users.insert_one(userDetails)
    user_details = get_user_details(userDetails['username'])[0]
    course_details = get_courses_details(userDetails['username'])
    return {
        "status_code": 200,
        "message": "Account Created",
        "data": {
            'user_details': user_details,
            'course_details': course_details
        }
    }

@app.route('/login', methods = ['POST'])
def user_login():
    body = request.data
    userDetails = json.loads(body)
    print(userDetails)
    targetUser = list(db.users.find(
        {
            "$and": 
            [ 
                {"username": userDetails['username']},
                {"password":  userDetails["password"]}
            ]
        }
    ))
    print(targetUser)
    if(len(targetUser) == 0):
        return {
            'status_code': 400,
            'message': "Invalue username or password",
            'data': []
        }
    targetUser = targetUser[0]
    del targetUser['_id']
    course_details = get_courses_details(userDetails['username'])
    return {
        "status_code": 200,
        "message": "Successfull",
        "data": {
            'user_details': targetUser,
            'course_details': course_details
        }
    }

@app.route('/upload', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return {}
        file = request.files['file']
        content = file.read()
        f = open(file.filename, 'wb')
        f.write(content)
        f.close()
        print(content)
        return {}
    
@app.route('/regiter_course', methods = ['POST'])
def register_new_course():
    course_data = request.json
    print(course_data)
    current_exist_course = query_course_details({
        "$and": [
            {
                "username": course_data['username']
            },
            {
                "course_code": course_data['course_code']
            }
        ]
    })
    print(current_exist_course)
    if len(current_exist_course) > 0:
        return {
            'status_code': 400,
            'message': "Course code already exists",
            'data': {

            }
        }
    db.courses.insert_one(course_data)
    return {
        'status_code': 200,
        'message': 'Successfull',
        'data': {

        }
    }

app.run(host = "0.0.0.0")