import psycopg2
import psycopg2.extras

# Py-linq part
def connectToRK():
    try:
        connect = psycopg2.connect\
        (
            database = "rk3",
            user = "postgres",
            password = '1&0O#_)"d',
            host = "127.0.0.1",
            port = "5432"
        )
        return connect
    except:
        return None

def getCursor(connection):
    cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
    return cursor

def OldestFinEmp():
    try:
        cursor.execute\
        (
            '''
            select fio, age(birthday) ag
            from emps
            where dep = 'Бухгалтерия'
            order by ag desc
            limit 1
            '''
        )
        result = cursor.fetchone()
        print(result)
        return True
    except:
        return False

def exitMoreThanThreeTimes():
    try:
        cursor.execute\
        (
            '''
                select fio
                from 
                (
                    select row_number() over (partition by emp) cn, emp
                                from ctrl
                                where typ = 2
                ) asd join emps
                on asd.emp = emps.id
                where cn = 4
            '''
        )
        result = cursor.fetchall()
        print(result)
        return True
    except:
        return False

def cameLast():
    try:
        cursor.execute\
        (
            '''
                select fio, stime
                from 
                (
                    select row_number() over (partition by emp order by stime asc) rc, emp, stime, typ
                    from ctrl
                    where typ = 1
                ) asd join emps
                on asd.emp = emps.id
                where asd.rc = 1
                order by stime desc
                limit 1
            '''
        )
        result = cursor.fetchone()
        print(result)
        return True
    except:
        return False

# SQL Alchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer,\
                       String, Date, DateTime, Time, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker

def OldestFinEmpORM(session, emps):
    sub_query = session.query(emps.c.dep, func.min(emps.c.birthday)\
                       .label('emp_old'))\
                       .filter(emps.c.dep == 'Бухгалтерия')\
                       .group_by(emps.c.dep)\
                       .subquery()
    main_query = session.query(emps.c.id, emps.c.fio, emps.c.birthday,
                               emps.c.dep, sub_query.c.emp_old)\
                        .join(sub_query, emps.c.birthday == sub_query.c.emp_old 
                        and emps.c.dep == sub_query.c.dep)
    if not main_query.all():
        return False
    for res in main_query.all():
        print(res)
    print()
    return True

def exitMoreThanThreeTimesORM(session, emps, ctrl):
    sub_query = session.query(ctrl.c.emp, ctrl.c.sdate, func.count('*').label('out_count')) \
                   .filter(ctrl.c.typ == 2 and ctrl.c.typ == '2020-12-19') \
                   .group_by(ctrl.c.emp, ctrl.c.sdate).having(func.count('*') > 0) \
                   .subquery()
    main_query = session.query(emps.c.id, emps.c.fio, sub_query.c.out_count) \
                        .join(sub_query, emps.c.id == sub_query.c.emp)
    if not main_query.all():
        return False
    for res in main_query.all():
        print(res)
    print()
    return True

# Interface
def menu(connection, cursor, session, emps, ctrl):
    option = int(input())
    if option > 6 or option < 0:
        print("Wrong option\n")
        return True
    elif not option:
        cursor.close()
        connection.close()
        return False
    elif option == 1:
        state = OldestFinEmp()
        if not state:
            print("Smth went wrong")
            cursor.close()
            connection.rollback()
        return state
    elif option == 2:
        state = exitMoreThanThreeTimes()
        if not state:
            print("Smth went wrong")
            cursor.close()
            connection.rollback()
        return state
    elif option == 3:
        state = cameLast()
        if not state:
            print("Smth went wrong")
            cursor.close()
            connection.rollback()
        return state
    elif option == 4:
        state = OldestFinEmpORM(session, emps)
        if not state:
            print("Smth went wrong")
        return state
    elif option == 5:
        state = exitMoreThanThreeTimesORM(session, emps, ctrl)
        if not state:
            print("Smth went wrong")
        return state
    elif option == 6:
        # state = 
        if not state:
            print("Smth went wrong")
        return state

if __name__ == '__main__':
    connect = connectToRK()
    # ORM setup part
    engine = create_engine('postgresql+psycopg2://postgres:1&0O#_)"d@localhost/rk3', 
    executemany_mode='batch')
    conn = engine.raw_connection()
    meta = MetaData()
    ctrl = Table\
    (
        'ctrl',
        meta, 
        Column('emp', Integer), 
        Column('sdate', Date),
        Column('week_day', String),
        Column('stime', Time),
        Column('typ', Integer)
    )
    emps = Table\
    (
        'emps', 
        meta, 
        Column('id', Integer, primary_key = True), 
        Column('fio', String),
        Column('birthday', Date),
        Column('dep', String) 
    )
    # Start session
    
    Session = sessionmaker(bind = engine)
    session = Session()
    if connect != None:
        cursor = getCursor(connect)
        state = True
        while(state):
            print("Menu:")
            print("1 -- Olders fin dep employee")
            print("2 -- Employees who left > 3 times")
            print("3 -- Employee who came last today")
            print("4 -- Olders fin dep employee orm realization")
            print("5 -- Employees who left > 3 times orm realization")
            print("6 -- Employee who came last today orm realization")
            state = menu(connect, cursor, session, emps, ctrl)