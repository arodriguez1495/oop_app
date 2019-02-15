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
c.execute("CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY,dni INT SECONDARY KEY,first_name TEXT,last_name TEXT, group_id INT, FOREIGN KEY(group_id) REFERENCES groups(id))")
c.execute("CREATE TABLE IF NOT EXISTS teachers(id INTEGER PRIMARY KEY,dni INT SECONDARY KEY,first_name TEXT,last_name TEXT, username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS admin_users(id INTEGER PRIMARY KEY, dni INT SECONDARY KEY,first_name TEXT,last_name TEXT, username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY, max_members INT, schedule TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS subjects(id INTEGER PRIMARY KEY,name TEXT,teacher_id INT,course TEXT,campus TEXT,semester TEXT, group_id INT, FOREIGN KEY(teacher_id) REFERENCES teachers(id), FOREIGN KEY(group_id) REFERENCES groups(id))")
c.execute("CREATE TABLE IF NOT EXISTS grades(student_id INT,subject_id INT,grade REAL,FOREIGN KEY(student_id) REFERENCES students(id), FOREIGN KEY(subject_id) REFERENCES subjects(id))")
c.execute("CREATE TABLE IF NOT EXISTS intermediario(id INTEGER PRIMARY KEY, student_id INT, subject_id INT, FOREIGN KEY(student_id) REFERENCES students(id), FOREIGN KEY(subject_id) REFERENCES subjects(id))")


# Populate database with dummy records
dummy_fnames = ["Alejandro", "Ramiro", "Omar", "Juan", "Luis", "Gonzalo"]
dummy_lnames = ["Guerrero", "Cueva", "Trauco", "Farfan", "Gallese", "Yotun"]

# students
for i in range(20):
    # If id value is not given its value autoincrements
    dni = 70000000 + i
    first_name = dummy_fnames[random.randint(0,len(dummy_fnames)-1)]
    last_name = dummy_lnames[random.randint(0,len(dummy_fnames)-1)]
    group_id = random.randint(1,10)
    c.execute("INSERT INTO students (dni, first_name, last_name, group_id) VALUES (?, ?, ?, ?)",
               (dni, first_name, last_name, group_id))

# teachers
for i in range(5):
    # If id value is not given its value autoincrements
    dni = 70000000 + i
    first_name = dummy_fnames[random.randint(0,len(dummy_fnames)-1)]
    last_name = dummy_lnames[random.randint(0,len(dummy_fnames)-1)]
    username = first_name[0].lower() + "." + last_name.lower() + str(i)
    password = "12345"
    c.execute("INSERT INTO teachers (dni, first_name, last_name, username, password) VALUES (?, ?, ?, ?, ?)",
               (dni, first_name, last_name, username, password))

# groups
schedules = ['mañana', 'tarde', 'noche']
for i in range(10):
    # If id value is not given its value autoincrements
    max_members = random.randint(10,15)
    schedule = schedules[random.randint(0,2)]
    c.execute("INSERT INTO groups (max_members, schedule) VALUES (?, ?)",
               (max_members, schedule))

# subjects
subjects_names = [("Finanzas", "Finanzas"), ("Programación", "Ciencias de la computación"),
                  ("Filosofía", "Filosofía"), ("Artes", "Artes"),
                  ("Matemáticas", "Matemáticas"), ("Español", "Idiomas"),
                  ("Alemán", "Idiomas"), ("Inglés", "Idiomas"),
                  ("Álgebra Lineal", "Matemáticas"), ("Algoritmos", "Ciencias de la Computación")]
campus_name = ["A", "B", "C"]
semester_name = ["2017-1", "2017-2", "2018-0", "2018-1", "2018-2", "2019-0"]
for i in range(10):
    # If id value is not given its value autoincrements
    name = subjects_names[i][0]
    teacher_id = random.randint(1,5)
    course = subjects_names[i][1]
    campus = campus_name[random.randint(0,len(campus_name)-1)]
    semester = semester_name[random.randint(0,len(semester_name)-1)]
    c.execute("INSERT INTO subjects (name, teacher_id, course, campus, semester) VALUES (?, ?, ?, ?, ?)",
               (name, teacher_id, course, campus, semester))

import pandas as pd
grades_rels = []
# grades
for i in range(60):
    student_id = random.randint(1,20)
    subject_id = random.randint(1,10)
    grade = round(random.random()*20,2)
    grades_rels.append([student_id, subject_id])

    c.execute("INSERT INTO grades (student_id, subject_id, grade) VALUES (?, ?, ?)",
               (student_id, subject_id, grade))

# admin (just one admin user)
c.execute("INSERT INTO admin_users(dni, first_name, last_name, username, password) VALUES (70000090, 'Luis', 'Romero', 'l.romero0', 'admin')")

# intermediario
intermediario_df = pd.DataFrame(grades_rels, columns=['student_id', 'subject_id'])
for student_id in range(1,21):
    student_subjects = intermediario_df[intermediario_df['student_id'] == student_id]['subject_id'].values.tolist()
    if len(student_subjects) > 0:
        for subject_id in student_subjects:
            c.execute("INSERT INTO intermediario (student_id, subject_id) VALUES (?, ?)", (student_id, subject_id))
    else:
        for i in range(5):
            subject_id = random.randint(1,12)
            c.execute("INSERT INTO intermediario (student_id, subject_id) VALUES (?, ?)", (student_id, subject_id))

# Make changes in the database
conn.commit()

def read_from_db(table_name):
    '''This function print the whole table in database'''
    print(table_name)
    c.execute('SELECT * FROM {}'.format(table_name))
    for row in c.fetchall():
        print(row)

# View tables
read_from_db('teachers')
read_from_db('students')
read_from_db('groups')
read_from_db('subjects')
read_from_db('grades')
read_from_db('intermediario')


# Close cursos and connection to database
c.close()
conn.close()
