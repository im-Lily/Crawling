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


# 메인 이미지 url DB 추가
def save_main_data(imgUrlDict):
    conn, cursor = connect_db()

    print(">", imgUrlDict)

    query = f"INSERT INTO main_img (MAIN_IMG_URL, MAIN_IMG_ID) VALUES (\'{imgUrlDict['mainImageUrl']}\', \'{imgUrlDict['mainImageId']}\')"

    print("query1 : ", query)
    cursor.execute(query)

    cursor.execute(query)
    conn.commit()
    conn.close()


# 상세 이미지 url DB 추가
def save_detail_data(imgUrlDict):
    conn, cursor = connect_db()

    query = f"INSERT INTO detail_img (DETAIL_IMG_URL, MAIN_IMG_ID) VALUES (\'{imgUrlDict['detailImageUrl']}\', \'{imgUrlDict['mainImageId']}\')"
    print("query2: ", query)

    cursor.execute(query)
    conn.commit()
    conn.close()

# if __name__ == "__main__":
#     save_data()
