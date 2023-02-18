import logging
import sys

import pymysql

import imgUrl


# DB 연결
def connect_db():
    try:
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="root1234",
            db="hotel",
            charset="utf8")
        cursor = conn.cursor()
    except:
        logging.error("DB 연결 실패")
        sys.exit(1)

    return conn, cursor


def main():
    conn, cursor = connect_db()

    query = "INSERT INTO img (IMG_URL) VALUES (%s)"
    val = imgUrl.img_url()

    cursor.executemany(query, val)
    conn.commit()


if __name__ == "__main__":
    main()
