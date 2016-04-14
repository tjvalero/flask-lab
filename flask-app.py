from os import chdir
from os.path import dirname

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# DEMO STUFF

@app.route('/')
def view_hello():
    return 'Hello World!'

@app.route('/demo-1')
def view_demo_1():
    return render_template('demo-1.html', name='Justin')

@app.route('/demo-2/<name>')
def view_demo_2(name):
    return render_template('demo-1.html', name=name)

@app.route('/demo-3')
def view_demo_3():
    names = ['Alice', 'Bob', 'Charlie']
    return render_template('demo-3.html', salutation='Roll call', names=names)

# STUDENT DIRECTORY APP

class Student:
    def __init__(self, first_name, last_name, username, majors, advisor):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.majors = majors
        self.advisor = advisor
    def __repr__(self):
        return 'Student(' + self.username + ')'
    def __str__(self):
        return 'Student(' + self.username + ')'
    def __hash__(self):
        return self.username
    def __eq__(self, other):
        return self.username == other.username

def get_data():
    students = []
    with open('students.csv') as fd:
        for line in fd.read().splitlines():
            name, username, majors, advisor = line.split('\t')
            last_name, first_name = name.split(', ')
            students.append(Student(first_name, last_name, username, majors, advisor))
    return sorted(students, key=(lambda s: s.username))

@app.route('/directory')
def view_directory():
    student_list = get_data()
    return render_template('directory.html', students = student_list)

@app.route('/directory/<username>')
def view_student(username):
    students = get_data()
    for student in students:
        if student.username == username:
            current_student = student
            student_index = students.index(student)
            prev = students[student_index - 1]
            if student != students[-1]:
                next = students[student_index + 1]
            if student == students[-1]:
                next = students[0]
            if student != students[0]:
                prev = students[student_index - 1]
            if student == students[0]:
                prev = students[-1]

    return render_template('student.html', student = current_student, prev_student = prev, next_student = next)

# DON'T TOUCH THE CODE BELOW THIS LINE

@app.route('/css/<file>')
def view_css(file):
    return send_from_directory('css', file)

if __name__ == '__main__':
    chdir(dirname(__file__))
    app.run(debug=True)
