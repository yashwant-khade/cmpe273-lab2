import uuid
from flask import Flask, escape, request, jsonify

app = Flask(__name__)

DB = {
    "students": [],
    "classes": []
}


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
    for x in DB["students"]:
        if str(x['id']) == student_id:
            return x, 200
    return "No student found with this ID", 200


@app.route('/classes', methods=['GET', 'POST'])
def add_class():
    if request.method == 'POST':
        name = request.get_json()['name']
        class_obj = Class(name).response()
        DB["classes"].append(class_obj)
        return jsonify(class_obj), 201
    if request.method == 'GET':
        return jsonify(DB["classes"]), 201


@app.route('/classes/<class_id>', methods=['GET'])
def get_class(class_id):
    print(DB["classes"], class_id)
    for x in DB["classes"]:
        if str(x['id']) == class_id:
            return x, 201
    return "No class found with this ID", 201


@app.route('/classes/<class_id>', methods=['PATCH'])
def add_student_to_class(class_id):
    for index, c in enumerate(DB["classes"]):
        if str(c['id']) == class_id:
            student_id = request.get_json()['student_id']
            for x in DB["students"]:
                if str(x['id']) == student_id:
                    DB["classes"][index]["students"].append(x)
                    return DB["classes"][index], 201
    return "The class or student could not be found with this ID", 201


# if __name__ == "__main__":
#     app.run(debug=True)
