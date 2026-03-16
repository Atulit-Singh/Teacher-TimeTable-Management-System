import pymysql
from datetime import datetime
import pandas as pd

pd.set_option('display.max_columns', None)


def get_panels(cursor, teacher_id, day):
    q = f"Select * from CSE.teacher_timetable where teacher_id = {teacher_id} and day_of_week = '{day}'"
    cursor.execute(q)
    res = cursor.fetchone()
    # df = pd.DataFrame(res)
    # print(df)
    print(res)
    slot_count = 1
    panels_teaching = []
    for i in range(2, 10):
        if res[i] != '':
            panels_teaching.append(res[i])
    print(panels_teaching)
    return panels_teaching


# def check_availability(teacher, old_teacher, weekday):


def get_teachers(cursor, panels_teaching, teacher_id):
    '''
    for panel in panels_teaching:
        query = f"Select teachers from cse.panel_data where Panel_name = '{panel}' and teachers != {teach_id}"
        cursor.execute(query)
        count = cursor.rowcount
        print(count)
        res = cursor.fetchall()
        print(res)
    '''

    q = f"Select teachers from cse.panel_data where Panel_name = '{panels_teaching[0]}' and teachers != {teacher_id}"
    cursor.execute(q)
    count = cursor.rowcount
    while count > 0:
        res = cursor.fetchone()
        print(res)
        teacher = res[0]
        print(teacher)
        count = count - 1


def main():
    host = 'localhost'
    user = 'root'
    password = 'root'
    database = 'university'

    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    cursor = connection.cursor()

    lid = input("Enter Leave ID: ")
    teach_id = input("Enter Teacher ID: ")
    # sdate = input("Enter Leave Start Date (yyyy-mm-dd): ")
    # edate = input("Enter leave end date: ")
    sdate = "2025-03-12"
    edate = "2025-03-12"

    query = f"Insert into leave_request values ({lid}, '{sdate}', '{edate}', {teach_id});"

    '''
    try:
        cursor.execute(q)
        date_obj = datetime.strptime(sdate, "%Y-%m-%d")
        weekday = date_obj.strftime("%A")
        print(weekday)

        panels_teaching = get_panels(teach_id, weekday)
        get_panels(panels_teaching, teach_id)




    except:
        print("ERROR IN Data")
    '''

    cursor.execute(query)
    date_obj = datetime.strptime(sdate, "%Y-%m-%d")
    weekday = date_obj.strftime("%A")
    print(weekday)

    panels = get_panels(cursor, teach_id, weekday)
    get_teachers(cursor, panels, teach_id)


main()
