import psycopg2
import psycopg2.extras

# DB connect/exit funcs
def connectToRE():
    try:
        connect = psycopg2.connect\
        (
            database = "Real_Estate",
            user = "postgres",
            password = '1&0O#_)"d',
            host = "127.0.0.1",
            port = "5432"
        )
        print("Database connected\n")
        return connect
    except:
        print("Failed to connect\n")
        return None

def getCursor(connection):
    # Use cursor with column names
    cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
    return cursor

def errorExit(connection, cursor):
    print("Error. Changes aborted. Close connection")
    cursor.close()
    connection.rollback()
    connection.close()

def normalExit(connection, cursor):
    print("Connection closed")
    cursor.close()
    connection.close()

# Actions
def getPriceByCadNum(CadNum, cursor):
    """Finds price of the realty in
    re_obj table of database.

    Args:
        CadNum (int): PK for realty object
        cursor (cursor): DB cursor to execute queries through
        
    Returns:
        flag: Indicator of execution
    """
    try:
        cursor.execute("select cad_value from re_obj where cad_num = {}".format(CadNum))
        result = cursor.fetchall()
        print("Price is " + str(result[0]['cad_value']) + " rubbles\n")
        return True
    except:
        return False

def getFullInfoByCadNum(CadNum, cursor):
    """Finds full information on the realty in
    re_obj table of database.

    Args:
        CadNum (int): PK for realty object
        cursor (cursor): DB cursor to execute queries through
        
    Returns:
        flag: Indicator of execution
    """
    try:
        cursor.execute\
        (
            '''select *
            from re_obj reo
            join re_ownership reow
            on reo.cad_num = reow.cad_num
            join re_owner ren
            on reow.ensurance_num = ren.ensurance_num
            join re_ownership_type reot
            on reow.ownership_type_id = reot.ownership_type_id 
            where reo.cad_num = {}'''.format(CadNum)
        )
        result = cursor.fetchall()
        print("Owners info:")
        for i in range(len(result)):
            print(result[i][9], end = '\t')
            print(result[i][11], end = '\t')
            print(result[i][12], end = '\t')
            print(result[i][10], end = '\n')
        print()
        print("Realty info:")
        print(result[0][0], end = '\t')
        print(result[0][3], end = '\t')
        print("{:<6}".format(result[0][4]), end = '')
        print("{:<11}".format(result[0][2]))
        print(result[0][1], end = '\n\n')
        print("Ownership info:")
        print(result[0][14], end = '\t')
        print(result[0][13], end = '\n\n')
        return True
    except:
        return False

def topFive(cursor):
    """Through the use of CTE and window
    functions find the persons with the most
    valueble properties and take five of them

    Args:
        CadNum (int): PK for realty object
        cursor (cursor): DB cursor to execute queries through
        
    Returns:
        flag: Indicator of execution
    """
    try:
        cursor.execute\
        ('''
            with toplist (person, val) as
            (
                select owner_name, sv
                from
                (
                    select distinct rr.ensurance_num nm, sum(cad_value)
                    over (partition by rr.ensurance_num) sv
                    from re_ownership rp join re_obj rj
                    on rp.cad_num = rj.cad_num join re_owner rr
                    on rr.ensurance_num = rp.ensurance_num
                    group by rr.ensurance_num, rj.cad_value
                ) as query join re_owner
                on re_owner.ensurance_num = nm
                order by sv desc
            )
            select person, val
            from toplist
            limit 5
            '''
        )
        result = cursor.fetchall()
        print("Top five persons with the most valuable property:")
        for i in range(5):
            print(i + 1, result[i][0] + '\t', result[i][1])
        print()
        return True
    except:
        return False    

def getTableInfo(tableName, cursor):
    """Get information about table of tableName
    from metadata and printed. If table does not exist it is
    not displayed

    Args:
        tableName (string): Name of the table to be displayed
        cursor (cursor): DB cursor to execute queries through

    Returns:
        flag: Indicator of execution
    """
    try:
        cursor.execute\
        (   '''
            select
            column_name,
            data_type,
            character_maximum_length,
            numeric_precision
            from information_schema.columns
            where table_schema not in ('information_schema','pg_catalog')
            and table_name = {}
            '''.format(tableName)
        )
        result = cursor.fetchall()
        if result == []:
            print("Table does not exist in database\n")
            return False
        else:
            print("Table {} info:".format(tableName))
            for i in range(len(result)):
                print("{:<28}".format(result[i]['column_name']), end = '')
                print(result[i]['numeric_precision'], end = '\t')
                print(result[i]['character_maximum_length'], end = '\t')
                print(result[i]['data_type'])
            return True
    except:
        return False

def getMaxValue(cursor):
    """Finds the maximum value of
    the property. Value is integer

    Args:
        cursor (cursor): DB cursor to execute queries through

    Returns:
        flag: Indicator of execution
    """
    try:
        cursor.execute("select maxObjValue()")
        result = cursor.fetchone()
        print("The maximum price is " + str(result[0]) + '\n')
        return True
    except:
        return False

def deleteMostExpensivePropertyByTypeName(typeName, connection, cursor):
    """Delete owners of the most 
    expensive property in chosen ownership type
    and show it in the console.

    Args:
        typeName (str): Name of the ownership type
        connection (DBconnection): Connection to commit or rollback changes
        cursor (cursor): DB cursor to execute queries through

    Returns:
        flag: Indicator of execution
    """
    try:
        cursor.execute\
        (
            '''
            select * from DeleteMostExpensivePropertyByType
            ({}) join owner_view
            on ensurance_num = ensurance
            '''.format(typeName)
        )
        result = cursor.fetchall()
        print("The owner of the most expensive property is\n{:<24}, {}".format(
        result[0]['owner_name'], result[0]['ensurance_num']))
        if result[0]['gender'] == 'муж.':
            print("He", end = ' ')
        else:
            print("She", end = ' ')
        print("owns " + str(len(result)) + " realty estates:")
        print("{:<15}\t{}".format("Cadasty Number", "Price"))
        for i in range(len(result)):
            print(result[i][1], end = '\t')
            print(result[i][2])
        print()
        #change to commit() when ready to actually update table
        connection.rollback()
        return True
    except:
        return False

def updatePriceForSquareMeter(newPrice, sqrL, sqrH, connection, cursor):
    """Changes all values in range from sqrL to sqrH
    to square * newPrice. Then show changes

    Args:
        newPrice (real): Price for one square meter
        sqrL (int): Left border for square
        sqrH (int): Right border for square
        connection (DBconnection): Connection to commit or rollback changes
        cursor (cursor): DB cursor to execute queries through

    Returns:
        flag: Indicator of execution
    """
    try:
        # Create a temp table
        cursor.execute\
        (
            '''
            select *
            into temp obj
            from re_obj
            '''
        )
        #connection.commit()
        # Called a stored procedure
        cursor.execute\
        (
            '''
            call update_price({},{},{})
            '''.format(newPrice, sqrL, sqrH)
        )
        connection.commit()
        # Show changes
        cursor.execute\
        (
            '''
            select re_obj.cad_value as newValue, obj.cad_value as OldValue
            from obj join re_obj on obj.cad_num = re_obj.cad_num
            where obj.obj_square between {} and {}
            order by obj.cad_value desc
            '''.format(sqrL, sqrH)
        )
        result = cursor.fetchall()
        print("Changed {} values:".format(str(len(result))))
        print("{:<12}\t{}".format("Old value","New value"))
        for i in range(len(result)):
            print("{:<12}".format(str(result[i][1])), end = '\t')
            print(result[i][0])
        print()
        return True
    except:
        return False

def getPostgresType(value, cursor):
    """Get Postgres type of any value

    Args:
        value (any): value to evaluate type of
        cursor (cursor): DB cursor to execute queries through

    Returns:
        flag: Indicator of execution
    """
    try:
        cursor.execute\
        # (
        #     '''
        #     select pg_typeof({})
        #     '''.format(value)
        # )
        ('''
        select pg_typof({})
            '''.format(value)
        )
        result = cursor.fetchone()
        print(result[0] + '\n')
        return True
    except psycopg2.errors.SyntaxError:
        print("Postgres can not recognise this data type,\ntry to use varchar\n")
        return False
    except:
        return False

# To include later 
# https://www.legalzoom.com/articles/10-terms-to-include-in-your-rental-agreement
def createRentTable(connection, cursor):
    try:
        cursor.execute\
        (
            '''
            create table if not exists rent
            (
                id serial not null primary key,
                cad_num bigint references re_obj(cad_num),
                tenant serial references tenants(id),
                to_pay real,
                paid real
            )
            '''
        )
        connection.commit()
        print("Table created\n")
        return True
    except:
        return False

def destructRentTable(connection, cursor):
    try:
        cursor.execute("drop table rent")
        connection.commit()
        print("Table dropped\n")
        return True
    except:
        return False

def addRent(cadNum, tenant_id, paid, to_pay, connection, cursor):
    try:
        # Realty estate can not be rented if it has more than
        # one owner
        cursor.execute\
        (
            '''
            select ownership_type_id
            from re_ownership
            where cad_num = {}
            '''.format(cadNum)
        )
        result = cursor.fetchone()
        if result[0] > 1:
            print("This property can not be rented\n")
            return False
        else:
            cursor.execute("select info->> 'name' from tenants where id = {}".format(tenant_id))
            result = cursor.fetchone()
            if result == None:
                print("Tenant not found\n")
                return False
            else:
                print("{} is now renting {}\nand charged for {}, instantly paid {}\n".format(result[0], cadNum, to_pay, paid))
                cursor.execute\
                (
                    '''
                    insert into rent(cad_num, tenant, to_pay, paid)
                    values({},{},{},{})
                    '''.format(cadNum, tenant_id, to_pay, paid)
                )
                connection.rollback()
                # connection.commit()
                return True
    except:
        print("Error while iserting values to rent table\n")
        return False

def optionHandler(option, connection, cursor):
    if option > 10:
        print("Wrong option\n")
        return True
    elif not option:
        normalExit(connect, cursor)
        return False
    elif option == 1:
        cadNum = int(input("Enter cadastry number of the real-estate: "))
        status = getPriceByCadNum(cadNum, cursor)
        # if not status:
        #     errorExit(connect, cursor)
        #     return False
        return True
    elif option == 2:
        cadNum = int(input("Enter cadastry number of the real-estate: "))
        status = getFullInfoByCadNum(cadNum, cursor)
        # if not status:
        #     errorExit(connect, cursor)
        #     return False
        return True
    elif option == 3:
        status = topFive(cursor)
        # if not status:
        #     errorExit(connect, cursor)
        #     return False
        return True
# getPostgresType(value, cursor)
    elif option == 4:
        tableName = input("Enter table name: ")
        tableName = "'{}'".format(tableName)
        status = getTableInfo(tableName, cursor)
        # if not status:
        #     errorExit(connect, cursor)
        #     return False
        return True
    elif option == 5:
        state = getMaxValue(cursor)
        # if not status:
        #     errorExit(connect, cursor)
        #     return False
        return True
    elif option == 6:
        print("Choose the type of ownership:")
        print("1 -- Индивидуальная собственность")
        print("2 -- Долевая собственность")
        print("3 -- Общая долевая собственность")
        print("4 -- Общая совместная собственность")
        chosen = int(input())
        if chosen == 1:
            typeName = "'Индивидуальная собственность'"
        elif chosen == 2:
            typeName = "'Долевая собственность'"
        elif chosen == 3:
            typeName = "'Общая долевая собственность'"
        elif chosen == 4:
            typeName = "'Общая совместная собственность'"
        else:
            return True
        status = deleteMostExpensivePropertyByTypeName(typeName, connection, cursor)
        if not status:
            errorExit(connect, cursor)
            return False
        return True
    elif option == 7:
        newPrice = int(input("Enter new price for square meter: "))
        sqrL = int(input("Enter square left  border of selected property: "))
        sqrH = int(input("Enter square right border of selected property: "))
        status = updatePriceForSquareMeter(newPrice, sqrL, sqrH, connection, cursor)
        if not status:
            errorExit(connect, cursor)
            return False
        return True
    elif option == 8:
        print("Choose the type of your input:")
        print("1 -- string")
        print("2 -- integer")
        print("3 -- float number")
        chosen = int(input())
        if chosen == 1:
            value = input("Enter string value: ")
        elif chosen == 2:
            value = int(input("Enter integer value: "))
        elif chosen == 3:
            value = float(input("Enter float value: "))
        else:
            return True
        status = getPostgresType(value, cursor)
        if not status:
            errorExit(connect, cursor)
            return False
        return True
    elif option == 9:
        status = createRentTable(connect, cursor)
        if not status:
            errorExit(connect, cursor)
            return False
        return True
    elif option == 10:
        cadNum = int(input("Enter cadastry number of the real-estate: "))
        tenant_id = int(input("Enter tenant id number: "))
        to_pay = float(input("Enter value of payment: "))
        paid = float(input("Enter value of paid sum: "))
        status = addRent(cadNum, tenant_id, paid, to_pay, connect, cursor)
        if not status:
            errorExit(connect, cursor)
            return False
        return True

# Console interface
def menu(connection, cursor):
    print('+' + '-' * 78 + '+')
    print("|     {:<73}".format("Menu") + '|')
    print('+' + '-' * 78 + '+')
    print("| 0.  {:<73}".format("Exit") + '|')
    print("| 1.  {:<73}".format("Scalar query") + '|')
    print("| 2.  {:<73}".format("Multijoin query") + '|')
    print("| 3.  {:<73}".format("CTE and window functions query") + '|')
    print("| 4.  {:<73}".format("Metadata query") + '|')
    print("| 5.  {:<73}".format("Scalar function call") + '|')
    print("| 6.  {:<73}".format("Multioperator function call") + '|')
    print("| 7.  {:<73}".format("Stored procedure call") + '|')
    print("| 8.  {:<73}".format("System function call") + '|')
    print("| 9.  {:<73}".format("Creete table on DB") + '|')
    print("| 10. {:<73}".format("Insert into table") + '|')
    print('+' + '-' * 78 + '+')
    print("Choose an option: ")
    option = int(input())
    return optionHandler(option, connection, cursor)
    
if __name__ == "__main__":
    connect = connectToRE()
    if connect != None:
        cursor = getCursor(connect)
        state = True
        while(state):
            state = menu(connect, cursor)
        # 824599521407922 is the cad_num of the first element of re_obj
        # getPriceByCadNum(824599521407922, cursor)
        # getFullInfoByCadNum(824599521407922, cursor)
        # topFive(cursor)
        # getTableInfo("'table'", cursor)
        # getMaxValue(cursor)
        # deleteMostExpensivePropertyByTypeName(
        # "'Индивидуальная собственность'", connect, cursor)
        # updatePriceForSquareMeter(5000, 100, 200, connect, cursor)
        # getPostgresType('10.10', cursor)
        # createRentTable(connect, cursor)
        # destructRentTable(connect, cursor)
        # 443315876273126 -- ownership_type_id = 1, one owner possible
        # addRent(443315876273126, 16, 100, 200, connect, cursor)
