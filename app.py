from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


import pymysql
import json




@app.route('/')
def mypage():
    return render_template('mypage.html')



@app.route("/mypage", methods=['GET'])
def feed_get():
    db = pymysql.connect(host='localhost', user='root', db='mapaltofu', password='xK7C8r9nJF', charset='utf8')
    curs = db.cursor()

    sql = """
    select * 
    from feed
    """
    curs.execute(sql)

    rows = curs.fetchall()

    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
    db.commit()
    db.close()
    return json_str, 200





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

