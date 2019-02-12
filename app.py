import sqlite3
import pandas as pd
from teacher import Teacher
from classes import Admin

#c.execute('SELECT * FROM admin_users')
#c.fetchall()
#c.execute('SELECT * FROM teachers')
#c.fetchall()[0]

def authentication():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    print('Hi, please insert your credentials')
    username = input('Username:')
    password = input('Password:')
    #c.execute('SELECT count(*) FROM teachers WHERE username = "{}" AND password  = "{}"'.format(username,password))
    #count = c.fetchall()[0][0]
    #if count == 1:
    c.execute('SELECT id, username, password, first_name, last_name FROM teachers WHERE username = "{}" AND password  = "{}"'.format(username,password))
    data_readed = c.fetchall()
    if len(data_readed)>0:
        user_data = data_readed[0]
        current_user = Teacher(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
        c.close()
        conn.close()
        return current_user
    else:
        c.execute('SELECT id, username, password, first_name, last_name FROM admin_users WHERE username = "{}" AND password  = "{}"'.format(username,password))
        data_readed = c.fetchall()
        if len(data_readed)>0:
            user_data = data_readed[0]
            current_user = Teacher(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
            c.close()
            conn.close()
            return current_user
        else:
            c.close()
            conn.close()
            return print('No user found')

def teacher_app(user):
    print("""
        1. Actas de asignaturas\n
        2. Consultas de alumnos\n
        3. Estadisticas de calificaciones\n
    """)
    sel_menu_0 = input()
    if sel_menu_0 == 1:
        print("""
            1. Actas por asignaturas\n
            2. Integrar grupos por asginatura\n
            3. Volver al menu inicial
            """)
        sel_menu_1_1 = input()
        if sel_menu_1_1 == 1: user.get_records()
        elif sel_menu_1_1 == 2: user.get_records(grouped=True)
        elif sel_menu_1_1 == 3: teacher_app(user)

        print("""
        1. Completar notas\n
        2. Anadir un alumno\n
        3. Borrar un alumno\n
        4. Exportar acta\n
        5. Importar acta\n
        6. Imprimir acta y lista provisional de alumnos\n
        7. Volver al menu inicial
        """)
        sel_menu_1_2 = input()
        if sel_menu_1_2 == 1: user.set_grades(subject_id, student_id, grade)
        elif sel_menu_1_2 == 2: user.add_student(subject_id, student_id)
        elif sel_menu_1_2 == 3: user.remove_student(subject_id, student_id)
        elif sel_menu_1_1 == 1 and sel_menu_1_2 == 4: user.export_records()
        elif sel_menu_1_1 == 2 and sel_menu_1_2 == 4: user.export_records(grouped=True)
        elif sel_menu_1_1 == 1 and sel_menu_1_2 == 5: user.import_records()
        elif sel_menu_1_1 == 2 and sel_menu_1_2 == 5: user.import_records(grouped=True)
        elif sel_menu_1_2 == 6: user.print_records()

    elif sel_menu_0 == 2: user.get_student_info(student_id)

    elif sel_menu_0 == 3: user.get_statistics()

current_user = authentication()
if type(current_user) == Teacher: teacher_app(current_user)
elif type(current_user) == Admin: admin_app(current_user)
else: 'Closing app ...'


##################### MUST LOCATE THIS FUNCTION IN THE CORRECT CLASS

def build_blank_record():
    blank_head = pd.DataFrame(index=["Course", "Campus", "Nombre", "Semester", "Group"])
    blank_grades = pd.DataFrame(columns=["ID","DNI","First Name","Last Name","Grade"])

    writer = pd.ExcelWriter('example-record.xlsx', engine='xlsxwriter')
    c.fetchall()
    blank_head.to_excel(writer, sheet_name='Course1')
    blank_grades.to_excel(writer, index=False, startrow=len(blank_head.index)+2, sheet_name='Course1')

    writer.save()

##################### MUST LOCATE THIS FUNCTION IN THE CORRECT CLASS
