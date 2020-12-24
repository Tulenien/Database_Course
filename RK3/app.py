import psycopg2
import psycopg2.extras

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
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, Time, BigInteger
from sqlalchemy.sql import func

def menu(connection, cursor):
    option = int(input())
    if option > 4 or option < 0:
        print("Wrong option\n")
        return True
    if not option:
        cursor.close()
        connection.close()
    if option == 1:
        state = OldestFinEmp()
        if not state:
            print("Smth went wrong")
            cursor.close()
            connection.rollback()
            return False
        return state
    elif option == 2:
        state = exitMoreThanThreeTimes()
        if not state:
            print("Smth went wrong")
            cursor.close()
            connection.rollback()
            return False
        return state
    elif option == 3:
        state = cameLast()
        if not state:
            print("Smth went wrong")
            cursor.close()
            connection.rollback()
            return False
        return state
    elif option == 4:
        # state = 
        if not state:
            print("Smth went wrong")
            return False
        return state
    elif option == 5:
        # state = 
        if not state:
            print("Smth went wrong")
            return False
        return state
    elif option == 6:
        # state = 
        if not state:
            print("Smth went wrong")
            return False
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
            state = menu(connect, cursor)