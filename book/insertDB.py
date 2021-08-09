import sys
import os
import rds_auth
import pymysql
import logging
import time

sys.path.insert(0,'./Users/dmsru/Desktop/shopping/book/rds_auth.py')
login = rds_auth.Info

def connect_RDS() :
    try :
        conn = pymysql.connect(
        host=login['host_name'],
        port=login['port'],
        user=login['user_name'], 
        passwd=login['password'],
        db=login['database_name'],
        charset="utf8")
        cursor = conn.cursor()
    except :
        logging.error("RDS 연결 실패")
        sys.exit(1)

    return conn, cursor

def main() :
    conn, cursor = connect_RDS()

    query = "INSERT INTO Book (book_id, book_nm, writer, thumbnail_url, book_info_url, price) VALUES (4,'a','b','c','d',5)"
    cursor.execute(query)
    conn.commit()

if __name__ == "__main__" :
    main()


