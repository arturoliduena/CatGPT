import psycopg2
from supabase.config import get_config


def connect():
    db = get_config('./config.ini', 'postgresql')
    try:
        conn = psycopg2.connect(
            "host='{host}' dbname='{dbname}' user='{user}' password='{password}' port=6543".format(host=db['host'], dbname=db['dbname'], user=db['user'], password=db['password']))
    except Exception as err:
        raise Exception("Can't connect to database:", err)
    return conn