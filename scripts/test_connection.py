import psycopg2

def postgres_test():

    try:
        conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres' connect_timeout=1")
        conn.close()
        print('success')
        return True
    except:
        print('fail')
        return False


postgres_test()
