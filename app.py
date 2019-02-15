# Dependencies
import sqlite3
import pandas as pd
from getpass import getpass
from teacher import Teacher
from admin import Admin
from record import Record
from group import Group

# Main functions
def authentication():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    print('Hola, por favor ingresa tus credenciales')
    username = input('Usuario: ')
    password = getpass('Contraseña: ')

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
            current_user = Admin(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
            c.close()
            conn.close()
            return current_user
        else:
            c.close()
            conn.close()
            return print('No user found')

def teacher_app(user):
    print("""
    Opciones disponibles:
        1. Actas de asignaturas\n
        2. Consultas de alumnos\n
        3. Estadisticas de calificaciones\n
    """)
    sel_menu_0 = int(input("Ingrese su seleccion: "))
    if sel_menu_0 == 1:
        user_record = Record(user.id)
        print("""
        Opciones disponibles:
            1. Actas por asignaturas\n
            2. Integrar grupos por asginatura\n
            3. Volver al menu inicial
            """)
        sel_menu_1_1 = int(input("Ingrese su seleccion: "))
        if sel_menu_1_1 == 1:
            user_record.get_records()
        elif sel_menu_1_1 == 2:
            user_record.get_records(grouped=True)
        elif sel_menu_1_1 == 3:
            teacher_app(user)

        print("""
        Opciones disponibles:
            1. Completar notas\n
            2. Anadir un alumno\n
            3. Borrar un alumno\n
            4. Exportar acta\n
            5. Importar acta\n
            6. Imprimir acta y lista provisional de alumnos\n
            7. Ver asginaturas de alumnos
            8. Volver al menu inicial
        """)
        sel_menu_1_2 = int(input("Ingrese su seleccion: "))
        if sel_menu_1_2 == 1: user.set_grades(input("Ingrese el id de la asignatura: "), input("Ingrese el id del estudiante: "), input("Ingrese la nota: "))
        elif sel_menu_1_2 == 2: user.add_student(input("Ingrese el id de la asignatura: "), input("Ingrese el id del estudiante: "))
        elif sel_menu_1_2 == 3: user.remove_student(input("Ingrese el id de la asignatura: "), input("Ingrese el id del estudiante: "))
        elif sel_menu_1_1 == 1 and sel_menu_1_2 == 4: user_record.get_records(export=True)
        elif sel_menu_1_1 == 2 and sel_menu_1_2 == 4: user_record.get_records(grouped=True, export=True)
        elif sel_menu_1_1 == 1 and sel_menu_1_2 == 5: user.import_records(input("Ingrese la ruta al archivo que desea importar\n(Formato: archivo excel tipo acta de una hoja):\n "))
        elif sel_menu_1_1 == 2 and sel_menu_1_2 == 5: user.import_records(input("Ingrese la ruta al archivo que desea importar\n(Formato: archivo excel tipo acta de una hoja):\n "), grouped=True)
        elif sel_menu_1_2 == 6: user_record.get_records(print_=True)
        elif sel_menu_1_2 == 7: user.get_students_subjects()
        teacher_app(user)

    elif sel_menu_0 == 2:
        user.get_student_info(input("Ingrese el id del estudiante: "))
        teacher_app(user)

    elif sel_menu_0 == 3:
        user.get_statistics(group_id=input("Ingrese el id del grupo: "), subject_id=input("Ingrese el id de la asignatura: "))
        teacher_app(user)

    teacher_app(user)

def admin_app(user):
    print('''
    Menu Inicial:
        1. Opciones de profesor\n
        2. Opciones de administrador\n
    Para salir de la aplicacion utilice Ctrl+C''')
    sel_menu_0 = int(input("Ingrese su selección: "))
    if sel_menu_0 == 1: teacher_app(user)
    elif sel_menu_0 == 2:
        print('''
        Opciones de administrador:
            1. Gestión ABMC alumnos\n
            2. Gestión ABMC asignaturas\n
            3. Gestión ABMC grupos\n
            4. Consulta de historial académico\n
            5. Volver al menú inicial''')
        sel_menu_1 = int(input("Ingrese su selección: "))
        if sel_menu_1 == 1:
            print(''' ¿Qué operación desea realizar?\n
                                1. Alta\n
                                2. Baja\n
                                3. Modificación\n
                                4. Consulta\n
                                5. Volver a menu inicial ''')
            action = int(input("Ingrese su selección: "))
            if action == 1: user.manage_students(operation='insert')
            elif action == 2: user.manage_students(operation='delete')
            elif action == 3: user.manage_students(operation='update')
            elif action == 4: user.manage_students(operation='select')

        elif sel_menu_1 == 2:
            print(''' ¿Qué operación desea realizar?\n
                                1. Alta\n
                                2. Baja\n
                                3. Modificación\n
                                4. Consulta\n
                                5. Volver a menu inicial ''')
            action = int(input("Ingrese su selección: "))
            if action == 1: user.manage_subjects(operation='insert')
            elif action == 2: user.manage_subjects(operation='delete')
            elif action == 3: user.manage_subjects(operation='update')
            elif action == 4: user.manage_subjects(operation='select')

        elif sel_menu_1 == 3:
            print(''' ¿Qué operación desea realizar?\n
                                1. Alta\n
                                2. Baja\n
                                3. Modificación\n
                                4. Consulta\n
                                5. Volver a menu inicial ''')
            action = int(input("Ingrese su selección: "))
            if action == 1: user.manage_groups(operation='insert')
            elif action == 2: user.manage_groups(operation='delete')
            elif action == 3: user.manage_groups(operation='update')
            elif action == 4: Group().get_groups(int(input("Ingrese el id del grupo que desea consultar: ")))

        elif sel_menu_1 == 4: user.get_historical_records(input("Ingrese el id del alumno: "))
        admin_app(user)

if __name__ == "__main__":
    current_user = authentication() # Ask user for credentials
    # Depending on user class give a different app view
    if type(current_user) == Teacher: teacher_app(current_user)
    elif type(current_user) == Admin: admin_app(current_user)
    else: 'Usuario no reconocido ... Cerrando aplicación  ...'
