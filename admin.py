import pandas as pd
from teacher import Teacher

class Admin(Teacher):

    def __init__(self, id, username, password, first_name, last_name):
            super().__init__(id, username, password, first_name, last_name)

    def manage_students(self, operation):
        if operation == 'insert':
            # Get user data
            # If id value is not given its value autoincrements
            dni = int(input("Ingrese el número de dni del nuevo alumno: "))
            first_name = input("Ingrese el nombre del nuevo alumno: ")
            last_name = input("Ingrese el apellido del nuevo alumno: ")
            group_id = int(input("Ingrese el id de grupo del nuevo alumno: "))
            values = (dni, first_name, last_name, group_id)
            # sql query
            sql = "INSERT INTO students(dni, first_name, last_name, group_id) VALUES (?, ?, ?, ?)"
            self.c.execute(sql, values)

        elif operation == 'delete':
            # Get user data
            id = input("Ingrese el id del alumno que desea borrar: ")
            # sql query
            sql = "DELETE FROM students WHERE id = ?"
            self.c.execute(sql, (id))

        elif operation == 'update':
            # Get user data
            id = int(input("Ingrese el id del alumno que desea modificar: "))
            dni = int(input("Ingrese el nuevo número de dni del alumno: "))
            first_name = input("Ingrese el nuevo nombre del alumno: ")
            last_name = input("Ingrese el nuevo apellido del alumno: ")
            group_id = int(input("Ingrese el nuevo id de grupo del alumno: "))
            values = (dni, first_name, last_name, group_id, id)
            # sql query
            sql = "UPDATE students SET dni = ?, first_name = ?, last_name = ?, group_id = ? WHERE id = ?"
            self.c.execute(sql, values)

        elif operation == 'select':
            # Get user data
            id = int(input("Ingrese el id del alumno que desea consultar: "))
            # sql query
            sql = "SELECT * FROM students WHERE id = {}".format(id)
            data = pd.read_sql(sql, self.conn)
            print(data.to_string(index=False))

        self.conn.commit()

        return print("operación realizada")

    def manage_subjects(self, operation):
        if operation == 'insert':
            # Get user data
            # If id value is not given its value autoincrements
            name = input("Ingrese el nombre de la nueva asignatura: ")
            teacher_id = int(input("Ingrese el id del profesor encargado de la nueva asignatura: "))
            course = input("Ingrese la carrera a la que pertenece la nueva asignatura: ")
            campus = input("Ingrese el campus donde se dictará la nueva asignatura: ")
            semester = input("Ingrese el semestre en el que se dictará la nueva asignatura: ")
            values = (name, teacher_id, course, campus, semester)
            # sql query
            sql = "INSERT INTO subjects(name, teacher_id, course, campus, semester) VALUES (?, ?, ?, ?, ?)"
            self.c.execute(sql, values)

        elif operation == 'delete':
            # Get user data
            id = int(input("Ingrese el id de la asignatura que desea borrar: "))
            # sql query
            sql = "DELETE FROM subjects WHERE id = ?"
            self.c.execute(sql, (id))

        elif operation == 'update':
            # Get user data
            id = int(input("Ingrese el id de la asignatura que desea modificar: "))
            name = input("Ingrese el nuevo nombre de la asignatura: ")
            teacher_id = int(input("Ingrese el id del nuevo profesor encargado de la asignatura: "))
            course = input("Ingrese la carrera a la que pertenece la asignatura: ")
            campus = input("Ingrese el campus donde se dictará la asignatura: ")
            semester = input("Ingrese el semestre en el que se dictará la asignatura: ")
            values = (name, teacher_id, course, campus, semester, id)
            # sql query
            sql = "UPDATE subjects SET name = ?, teacher_id = ?, course = ?, campus = ?, semester = ? WHERE id = ?"
            self.c.execute(sql, values)

        elif operation == 'select':
            # Get user data
            id = int(input("Ingrese el id de la asignatura que desea consultar: "))
            # sql query
            sql = "SELECT * FROM subjects WHERE id = {}".format(id)
            data = pd.read_sql(sql, self.conn)
            print(data.to_string(index=False))

        self.conn.commit()

        return print("operación realizada")

    def manage_groups(self, operation):
        if operation == 'insert':
            # Get user data
            # If id value is not given its value autoincrements
            max_members = int(input("Ingrese el número máximo de miembros del nuevo grupo: "))
            schedule = input("Ingrese el horario del nuevo grupo: ")
            values = (max_members, schedule)
            # sql query
            sql = "INSERT INTO groups(max_members, schedule) VALUES (?, ?)"
            self.c.execute(sql, values)

        elif operation == 'delete':
            # Get user data
            id = int(input("Ingrese el id del grupo que desea borrar: "))
            # sql query
            sql = "DELETE FROM groups WHERE id = ?"
            self.c.execute(sql, (id))

        elif operation == 'update':
            # Get user data
            id = int(input("Ingrese el id del grupo que desea modificar: "))
            max_members = int(input("Ingrese el nuevo número máximo de miembros del grupo: "))
            schedule = input("Ingrese el nuevo horario del grupo: ")
            values = (max_members, schedule, id)
            # sql query
            sql = "UPDATE groups SET max_members = ?, schedule = ? WHERE id = ?"
            self.c.execute(sql, values)

        elif operation == 'select':
            # Get user data
            id = int(input("Ingrese el id del grupo que desea consultar: "))
            # sql query
            sql = "SELECT * FROM groups WHERE id = {}".format(id)
            data = pd.read_sql(sql, self.conn)

            if data.shape[0] < 1: print("No existen grupos con ese id")
            else: print(data.to_string(index=False))

        self.conn.commit()

        return print("operación realizada")

    def get_historical_records(self, student_id):

        student_info = pd.read_sql('SELECT * FROM students WHERE id = {}'.format(student_id), self.conn) # Select specific student information
        print(student_info.to_string(index=False))

        grades = pd.read_sql('SELECT * FROM grades WHERE student_id = {}'.format(student_id), self.conn) # select specific student grades
        subjects = pd.read_sql('SELECT * FROM subjects', self.conn) # select all subjects
        merged = pd.merge(grades, subjects, how='left', left_on='subject_id', right_on='id') # get information about subject
        historical_record = merged[['semester', 'name', 'grade']].sort_values('semester') # get historical record in chronological order
        print(historical_record.to_string(index=False))

        return print('historical record printed')
