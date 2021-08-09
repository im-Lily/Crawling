import pymysql

host_name = "shop-book.ciclmc7wjq3o.ap-northeast-2.rds.amazonaws.com"
user_name = "shopmaster"
password = "springbook11"
database_name = "shop_book"

db = pymysql.connect(
    host=host_name,
    port=3306,
    user=user_name,
    passwd=password,
    db=database_name,
    charset="utf8"
)

cursor = db.cursor()

sql = "INSERT INTO Book (book_id, book_nm, writer, thumbnail_url, book_info_url, price) VALUES (%s, %s, %s, %s, %s, %s)"
val = (1,'a','b','c','d',2)
cursor.execute(sql, val)
db.commit()
db.close()

