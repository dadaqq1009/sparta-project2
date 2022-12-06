from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


import pymysql
import json




@app.route('/')
def mypage():
    db = pymysql.connect(host='localhost', user='root', db='mapaltofu', password='xK7C8r9nJF', charset='utf8')
    curs = db.cursor()

    sql = """
            select * 
            from feed as f
            LEFT JOIN `user` as u
            ON f.user_id = u.id
            """
    curs.execute(sql)
    rows = curs.fetchall()
    row = [list(rows[x] for x in range(len(rows)))]

    i_list = []
    for i in range(len(row)):
        i_list.insert(0,i)



    db.commit()
    db.close()
    return render_template('mypage.html', feed_list=row, num_list = i_list)



@app.route("/api/mypages", methods=['GET'])
def feed_get():
    db = pymysql.connect(host='localhost', user='root', db='mapaltofu', password='xK7C8r9nJF', charset='utf8')
    curs = db.cursor()

    # 여기 foreign key 방식으로 다시 써야됨!!!!
    sql = """
    select * 
    from feed as f
    LEFT JOIN `user` as u
    ON f.user_id = u.id
    """
    curs.execute(sql)
    rows = curs.fetchall()


    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
    db.commit()
    db.close()
    return json_str, 200
















if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

