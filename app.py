import sqlite3
import pandas as pd
from teacher import Teacher

def authentication():
    print('Hi, please insert your credentials')
    username = input('Username:')
    password = input('Password:')
    #c.execute('SELECT count(*) FROM teachers WHERE username = "{}" AND password  = "{}"'.format(username,password))
    #count = c.fetchall()[0][0]
    #if count == 1:
    c.execute('SELECT id, username, password, first_name, last_name FROM teachers WHERE username = "{}" AND password  = "{}"'.format(username,password))
    user_data = c.fetchall()[0]
    current_user = Teacher(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
    return current_user

current_user = authentication()

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
