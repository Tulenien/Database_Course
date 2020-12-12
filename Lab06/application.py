import psycopg2
import psycopg2.extras

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

def errorExit(connection):
    print("Error. Changes aborted. Close connection")
    connection.rollback()

def normalExit(connection):
    print("Connection closed")
    connection.close()

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

if __name__ == "__main__":
    connect = connectToRE()
    if connect != None:
        cursor = getCursor(connect)
        # 824599521407922
        getPriceByCadNum(824599521407922, cursor)
        getFullInfoByCadNum(824599521407922, cursor)
        normalExit(connect)