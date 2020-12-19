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

# Py-LINQ
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from py_linq import Enumerable

class Emps():
    def __init__(self, id, fio, birthday, dep):
        self.id = id
        self.fio = fio
        self.birthday = birthday
        self.dep = dep

class Ctrl():
    def __init__(self, id, emp, sdate, week_day, stime, typ):
        self.id = id
        self.emp = emp
        self.sdate = sdate
        self.week_day = week_day
        self.stime = stime
        self.typ = typ

def LambdaRealizationOldFinDep():
    try:
        engine = create_engine('postgresql+psycopg2://postgres:1&0O#_)"d@localhost/rk3', 
        executemany_mode='batch')
        connection = engine.connect()
        employees = connection.execute("select * from emps")
        controls = connection.execute("select * from ctrl")
        emps = Enumerable()
        ctrls = Enumerable()
        for elem in employees:
            emp = Emps(elem[0], elem[1], elem[2], elem[3])
            emps.append(emp)
        for elem in controls:
            ctrl = Ctrl(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5])
            ctrls.append(emp)
        # print(controls)
        # print(employees)
        oldest = emps.where(lambda x: x.dep == 'Бухгалтерия').order_by_descending(lambda x: x.birthday).select(lambda y: y.fio).last()
        # exits = 
        print("Oldest fin dep worker is {}".format(oldest))
        return True
    except:
        return False

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
        state = LambdaRealizationOldFinDep()
        if not state:
            print("Smth went wrong")
            return False
        return state


if __name__ == '__main__':
    connect = connectToRK()
    if connect != None:
        cursor = getCursor(connect)
        state = True
        while(state):
            print("Menu:")
            print("1 -- Olders fin dep employee")
            print("2 -- Employees who left > 3 times")
            print("3 -- Employee who came last today")
            print("4 -- Olders fin dep employee lambda realization")
            state = menu(connect, cursor)