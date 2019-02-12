class Student:

    def __init__(self, code, first_name, last_name):
        self.code = code
        self.first_name = first_name
        self.last_name = last_name

class Subject:

    def __init__(self, course, campus, name, semester, group, teacher=None):
        self.course = course
        self.campus = campus
        self.name = name
        self.semester = semester
        self.group = group
        self.teacher = teacher

class Admin:

    def __init__(self, id, username, password, first_name, last_name):
            self.id = id
            self.username = username
            self.password = password
            self.first_name = first_name
            self.last_name = last_name
