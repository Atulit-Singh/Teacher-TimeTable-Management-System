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
    panels_teaching = {}
    for i in range(2, 10):
        if res[i] != '':
            panels_teaching[slot_count] = res[i]
            slot_count += 1
        elif res[i] == '':
            slot_count += 1
    print(panels_teaching)

    return panels_teaching


def send_notification(cursor, new_teacher, slot, day, panel, date):
    print(f"\n\nYou are teacher {new_teacher}")
    print(
        f"Lecture is available on {day} for Panel {panel} in slot {slot}\nDo you want to accept to take the lecture? (y/n)")
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


def get_teachers(cursor, panels_teaching, teacher_id, day, date):

    for slot in panels_teaching:
        print(f"\n\nRESCHEDULING FOR PANEL {panels_teaching[slot]}\n")
        q = f"Select teachers from cse.panel_data where Panel_name = '{panels_teaching[slot]}' and teachers != {teacher_id} order by syllabus_completed_percentage"
        cursor.execute(q)
        count = cursor.rowcount
        print(count)
        all_teachers = cursor.fetchall()
        print(all_teachers)

        for res in all_teachers:
            teacher = res[0]
            print(teacher)
            check_availability(slot, teacher, cursor, day, panels_teaching[slot], date)
        # break


def ScheduleLeave(cursor):
    # lid = input("Enter Leave ID: ")
    teach_id = input("Enter Teacher ID: ")
    sdate = input("Enter Leave Start Date (yyyy-mm-dd): ")
    edate = input("Enter leave End Date (yyyy-mm-dd): ")
    # sdate = "2025-03-12"
    # edate = "2025-03-12"

    query = f"Insert into leave_request (start_date, end_date, teacher_id)values ('{sdate}', '{edate}', {teach_id});"


    cursor.execute(query)
    a = pd.date_range(start=sdate, end=edate)
    for date in a:
        print(date.date())
        date_obj = datetime.strptime(str(date.date()), "%Y-%m-%d")
        weekday = date_obj.strftime("%A")
        print(weekday)

        panels = get_panels(cursor, teach_id, weekday)
        get_teachers(cursor, panels, teach_id, weekday, sdate)


def AddTeacher(cursor):
    tid = int(input("ENTER TEACHER ID: "))
    teacher_name = str(input("ENTER TEACHER NAME: "))
    teacher_email = str(input("ENTER TEACHER EMAIL ID: "))
    teacher_contact = int(input("ENTER TEACHER CONTACT NUMBER: "))
    teacher_subject = str(input("ENTER SUBJECT TAUGHT BY TEACHER: "))
    lecture_count = int(input("ENTER WEEKLY LECTURE COUNT OF TEACHER: "))

    q = f"insert into university.teacher (teacher_id, name, email, phone_no, subject_taught, weekly_lecture_count) values ({tid}, '{teacher_name}', '{teacher_email}', {teacher_contact}, '{teacher_subject}', {lecture_count})"

    cursor.execute(q)


def AddTimeTable(cursor):
    tid = int(input("ENTER TEACHER ID: "))
    day = str(input("ENTER DAY NAME: "))
    slots = []
    for i in range (1,9):
        choice = int(input(F"ADD LECTURE IN SLOT {i}? 1/0: "))
        if choice == 1:
            inp = input(f"ENTER PANEL TEACHING IN SLOT {i}: ")
            slots.append(inp)
        else:
            slots.append('')

    q = f"INSERT INTO cse.teacher_timetable values({tid}, '{day}', '{slots[0]}', '{slots[1]}', '{slots[2]}', '{slots[3]}', '{slots[4]}', '{slots[5]}', '{slots[6]}', '{slots[7]}')"
    cursor.execute(q)


def addTeacherToPanel(cursor):
    pname = str(input("ENTER Panel Name: "))
    scount = int(input("ENTER Student Count: "))
    teacher = int(input("ENTER TEACHER ID OF TEACHER TEACHING: "))
    cr_name = str(input("ENTER NAME OF CR: "))

    q = f"insert into cse.panel_data (Student_Count, teachers, CR, Panel_name) values({scount}, {teacher}, '{cr_name}', '{pname}')"
    cursor.execute(q)


def main():
    host = ''
    user = ''
    password = ''
    database = ''

    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    cursor = connection.cursor()

    print("1. Schedule Leave\n2. Add new teacher\n3. Add new time table\n4. Add Teacher to Panel\nEnter Your Choice: ")
    choice = int(input())
    if choice == 1:
        ScheduleLeave(cursor)
    elif choice == 2:
        AddTeacher(cursor)
    elif choice == 3:
        AddTimeTable(cursor)
    elif choice == 4:
        addTeacherToPanel(cursor)
    else:
        print("INCORRECT CHOICE")




    connection.commit()


main()
