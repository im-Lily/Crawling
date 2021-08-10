import sys
import os
import rds_auth
import kyobo
import pymysql
import logging

# RDS 연결
sys.path.insert(0,'./rds_auth.py')
login = rds_auth.Info

# RDS 연결
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

    query = "INSERT INTO Book (book_nm,writer,publisher,price,isbn,thumbnail_url,description,section) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    val = kyobo.book_data()

    # query = "INSERT INTO Book (book_nm,writer,publisher,price,isbn,thumbnail_url) VALUES (%s,%s,%s,%s,%s,%s)"
    # val = kyobo.book_data()

    cursor.executemany(query,val)
    conn.commit()


if __name__ == "__main__" :
    main()