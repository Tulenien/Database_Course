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
    connection.rollback()

def normalExit(connection):
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
        print(str(result) + "\n")
        return True
    except:
        return False

if __name__ == "__main__":
    help(getPriceByCadNum)