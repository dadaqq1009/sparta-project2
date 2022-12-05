import pymysql


db = pymysql.connect(host = 'localhost',
                     port = 3306,
                     user = 'root',
                     passwd = 'Guswl1219',
                     db = 'mapaltofu',
                     charset = 'utf8')

cursor = db.cursor(pymysql.cursors.DictCursor)

# pymysql.cursors.DictCursor

cursor.execute('use mapaltofu;') # excute합수# 를 사용해 명령을 내림 / db 접근
# cursor.execute('insert into mapaltofu (id, name) values ("0", "한정훈")')
# cursor.execute('update mapaltofu set name="마팔두부" where name="한정훈"')
# cursor.execute('delete from mapaltofu where name="한정훈"')
# cursor.execute('insert into mapaltofu (id, name) values ("0", "한정훈")')

cursor.execute('select * from feed f;')
value = cursor.fetchall()
# print([value])
print([value[0]['title']])
# 마지막에 이게 꼭 나와야함
db.commit()
db.close()