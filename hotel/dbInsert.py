import datetime
import logging
import sys

import pymysql


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


def insert_review_data(review_data):
    conn, cursor = connect_db()

    now = datetime.datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    # 호텔 acco_id 조회
    select_query = ("select a.id from accommodation a where a.business_type = 'HOTEL' ORDER BY a.id;")
    cursor.execute(select_query)

    acco_ids = cursor.fetchall()  # 모든 호텔 id 조회

    query = f"INSERT INTO review (TITLE, RATING, CONTENT, REG_DT) VALUES (\'{review_data['title']}\', \'{review_data['rating']}\', \'{review_data['content']}\', %s)"
    val = (formatted_date)

    print("query1: ", query)

    cursor.execute(query, val)

    for acco_id in acco_ids:
        print("acco_id: ", acco_id[0])  # 튜플에서 각 값을 추출

        query = "UPDATE review SET ACCO_ID = %s WHERE DATE(REG_DT) = 20230309"
        val = (acco_id[0])
        cursor.execute(query, val)
    conn.commit()