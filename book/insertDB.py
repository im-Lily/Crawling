import sys
import os
import pymysql
import logging
import time

host_name = "shop-book.ciclmc7wjq3o.ap-northeast-2.rds.amazonaws.com"
port = 3306
user_name = "shopmaster"
password = "springbook11"
database_name = "shop_book"

def connect_RDS(host_name,port,user_name,password,database_name) :
    try :
        conn = pymysql.connect(
        host=host_name,
        port=port,
        user=user_name, 
        passwd=password,
        db=database_name,
        charset="utf8")
        cursor = conn.cursor()
    except :
        logging.error("RDS 연결 실패")
        sys.exit(1)

    return conn, cursor

def main() :
    conn, cursor = connect_RDS(host_name,port,user_name,password,database_name)

    query = "INSERT INTO Book (book_id, book_nm, writer, thumbnail_url, book_info_url, price) VALUES (2,'a','b','c','d',3)"
    cursor.execute(query)
    conn.commit()

if __name__ == "__main__" :
    main()


