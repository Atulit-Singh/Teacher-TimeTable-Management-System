import pymysql
from datetime import datetime
import pandas as pd

pd.set_option('display.max_columns', None)


def get_all_panels(cursor, teacher_id, day):
    q = f"Select * from CSE.teacher_timetable where teacher_id = {teacher_id} and day_of_week = '{day}'"
    cursor.execute(q)
    res = cursor.fetchone()
    # df = pd.DataFrame(res)
    # print(df)
    print(res)
    slot_count = 1
    panels_teaching = {}
    for i in range(2, 10):
        if res[i] != '':
            panels_teaching[slot_count] = res[i]
            slot_count += 1
        elif res[i] == '':
            slot_count += 1
    print(panels_teaching)
    '''
    for i in panels_teaching:
        print(panels_teaching[i], end= '\n')
    '''
    return panels_teaching


def get_panel(cursor, teacher_id, day, slot):
    q = f"Select slot_{slot} from CSE.teacher_timetable where teacher_id = {teacher_id} and day_of_week = '{day}'"
    cursor.execute(q)
    res = cursor.fetchone()
    print(res)
    return res[0]


def send_notification(cursor, new_teacher, slot, day, panel, date):
    print(f"\n\nYou are teacher {new_teacher}")
    print(f"Lecture is available on {day} for Panel {panel} in slot {slot}\nDo you want to accept to take the lecture? (y/n)")
    answer = input().lower()
    if answer == 'y':
        q = f"call cse.insert_reschedule({new_teacher}, '{day}', '{date}', {slot}, '{panel}');"
        cursor.execute(q)
        q = "select * from cse.rescheduled_lecture"
        cursor.execute(q)
        print(cursor.fetchone())


def check_availability(slot, new_teacher, cursor, day, panel, date):
    q = f"Select teacher_id from CSE.teacher_timetable where teacher_id = {new_teacher} and slot_{slot} = '' and day_of_week = '{day}';"
    cursor.execute(q)
    result = cursor.fetchone()
    if result is None:
        print(f"{new_teacher} TEACHER NOT FREE")
    else:
        print(f"{new_teacher} TEACHER IS FREE, SEND NOTIFICATION")
        send_notification(cursor, new_teacher, slot, day, panel, date)

    return


def get_teachers(cursor, panel_teaching, teacher_id, day, date, slot):
    '''
    for panel in panels_teaching:
        query = f"Select teachers from cse.panel_data where Panel_name = '{panel}' and teachers != {teach_id}"
        cursor.execute(query)
        count = cursor.rowcount
        print(count)
        res = cursor.fetchall()
        print(res)
    '''

    print(slot)
    q = f"Select teachers from cse.panel_data where Panel_name = '{panel_teaching}' and teachers != {teacher_id} order by syllabus_completed_percentage"
    cursor.execute(q)
    count = cursor.rowcount
    print(count)
    all_teachers = cursor.fetchall()
    print(all_teachers)

    for res in all_teachers:
        teacher = res[0]
        print(teacher)
        check_availability(slot, teacher, cursor, day, panel_teaching, date)
    #break


def main():
    host = ''
    user = ''
    password = ''
    database = ''

    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    cursor = connection.cursor()

    lid = input("Enter Leave ID: ")
    teach_id = input("Enter Teacher ID: ")
    # sdate = input("Enter Leave Start Date (yyyy-mm-dd): ")
    # edate = input("Enter leave end date: ")
    sdate = "2025-03-12"
    slot = 3

    #query = f"Insert into leave_request values ({lid}, '{sdate}', '{edate}', {teach_id});"

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

    #cursor.execute(query)
    date_obj = datetime.strptime(sdate, "%Y-%m-%d")
    weekday = date_obj.strftime("%A")
    print(weekday)

    #panels = get_all_panels(cursor, teach_id, weekday)
    panel = get_panel(cursor, teach_id, weekday, slot)
    get_teachers(cursor, panel, teach_id, weekday, sdate, slot)


main()
