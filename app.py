import uuid
from flask import Flask, escape, request, jsonify

app = Flask(__name__)

DB = {
    "students": [],
    "classes": []
}

# {
#     "id" : 1234456,
#     "name" : "Bob Smith"
# }
#
# {
#     "id": 1122334,
#     "name": "CMPE-273",
#     "students": []
# }


import json


class Student(object):
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()

    def response(self):
        temp = {
            "name": self.name,
            "id": self.id
        }
        return temp


class Class(object):
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self.students = []

    def response(self):
        return {
            "name": self.name,
            "id": self.id,
            "students": self.students
        }


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/students', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.get_json()['name']
        student_obj = Student(name).response()
        DB["students"].append(student_obj)
        return jsonify(student_obj), 201
    if request.method == 'GET':
        return jsonify(DB["students"]), 201


@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    print(DB["students"], student_id)
    for x in DB["students"]:
        if str(x['id']) == student_id:
            return x, 200
    return "No student found with this ID", 200


@app.route('/classes', methods=['GET', 'POST'])
def add_class():
    if request.method == 'POST':
        name = request.get_json()['name']
        class_obj = Class(name).response()
        DB["students"].append(class_obj)
        return jsonify(class_obj), 201
    if request.method == 'GET':
        return jsonify(DB["classes"]), 201


@app.route('/classes/<student_id>', methods=['GET'])
def get_class(student_id):
    print(DB["classes"], student_id)
    for x in DB["classes"]:
        if str(x['id']) == student_id:
            return x, 200
    return "No class found with this ID", 200


@app.route('/classes/<student_id>', methods=['PATCH'])
def add_class(student_id):
    for x in DB["students"]:
        if str(x['id']) == student_id:
            DB["classes"][0]["students"].append(x)
            return DB["classes"], 200
    return "No student found with this ID", 200


if __name__ == "__main__":
    app.run(debug=True)
