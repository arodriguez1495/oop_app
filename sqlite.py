# Dependencies
import sqlite3
import random
import os

# Restart sqlite3 db file
if 'school.db' in os.listdir(): os.remove('school.db')

# Sqlite connction
conn = sqlite3.connect('school.db')
c = conn.cursor()

# Create tables and relationships
c.execute("CREATE TABLE IF NOT EXISTS students(id INT PRIMARY KEY,dni INT SECONDARY KEY,first_name TEXT,last_name TEXT, group_id INT, FOREIGN KEY(group_id) REFERENCES groups(id))")
c.execute("CREATE TABLE IF NOT EXISTS teachers(id INT PRIMARY KEY,dni INT SECONDARY KEY,first_name TEXT,last_name TEXT, username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS admin_users(id INT PRIMARY KEY, dni INT SECONDARY KEY,first_name TEXT,last_name TEXT, username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS groups (id INT PRIMARY KEY, max_members INT, schedule TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS subjects(id INT PRIMARY KEY,name TEXT,teacher_id INT,course TEXT,campus TEXT,semester TEXT, group_id INT, FOREIGN KEY(teacher_id) REFERENCES teachers(id), FOREIGN KEY(group_id) REFERENCES groups(id))")
c.execute("CREATE TABLE IF NOT EXISTS grades(student_id INT,subject_id INT,grade REAL,FOREIGN KEY(student_id) REFERENCES students(id), FOREIGN KEY(subject_id) REFERENCES subjects(id))")

# Populate database with dummy records
dummy_fnames = ["Alejandro", "Ramiro", "Omar", "Juan", "Luis", "Gonzalo"]
dummy_lnames = ["Guerrero", "Cueva", "Trauco", "Farfan", "Gallese", "Yotun"]

# students
for i in range(20):
    id = i
    dni = 70000000 + i
    first_name = dummy_fnames[random.randint(0,len(dummy_fnames)-1)]
    last_name = dummy_lnames[random.randint(0,len(dummy_fnames)-1)]
    group_id = random.randint(0,9)
    c.execute("INSERT INTO students (id, dni, first_name, last_name) VALUES (?, ?, ?, ?)",
               (id, dni, first_name, last_name))

# teachers
for i in range(5):
    id = i
    dni = 70000000 + i
    first_name = dummy_fnames[random.randint(0,len(dummy_fnames)-1)]
    last_name = dummy_lnames[random.randint(0,len(dummy_fnames)-1)]
    username = first_name[0].lower() + "." + last_name.lower() + str(id)
    password = "12345"
    c.execute("INSERT INTO teachers (id, dni, first_name, last_name, username, password) VALUES (?, ?, ?, ?, ?, ?)",
               (id, dni, first_name, last_name, username, password))

# groups
schedules = ['morning','evening','night']
for i in range(10):
    id = i
    max_members = random.randint(10,15)
    schedule = schedules[random.randint(0,2)]
    c.execute("INSERT INTO groups (id, max_members, schedule) VALUES (?, ?, ?)",
               (id, max_members, schedule))

# subjects
subjects_names = [("Finance","Finance"), ("Programming","Computer Science"),
                  ("Philosophy", "Phylosophy"), ("Arts", "Arts"),
                  ("Mathematics","Mathematics"), ("Spanish","Language"),
                  ("German","Language"), ("English","Language"),
                  ("Linear Algebra","Mathematics"), ("Algorithms", "Computer Science")]

campus_name = ["A", "B", "C"]

semester_name = ["2018-1", "2018-2", "2019-0"]

for i in range(10):
    id = i
    name = subjects_names[i][0]
    teacher_id = random.randint(0,4)
    course = subjects_names[i][1]
    campus = campus_name[random.randint(0,2)]
    semester = semester_name[random.randint(0,2)]
    group_id = random.randint(0,10)
    c.execute("INSERT INTO subjects (id, name, teacher_id, course, campus, semester, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
               (id, name, teacher_id, course, campus, semester, group_id))

# grades
for i in range(60):
    student_id = random.randint(0,19)
    subject_id = random.randint(0,9)
    grade = round(random.random()*20,2)
    c.execute("INSERT INTO grades (student_id, subject_id, grade) VALUES (?, ?, ?)",
               (student_id, subject_id, grade))

# admin (just one admin user)
c.execute("INSERT INTO admin_users VALUES (0, 70000090, 'Luis', 'Romero', 'l.romero0', 'admin')")

conn.commit() # Make changes in the database

def read_from_db(table_name):
    '''This function print the whole table in database'''

    c.execute('SELECT * FROM {}'.format(table_name))
    for row in c.fetchall():
        print(row)

# View tables
read_from_db('teachers')
read_from_db('students')
read_from_db('groups')
read_from_db('subjects')
read_from_db('grades')

# Close cursos and connection to database
c.close()
conn.close()
