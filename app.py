from flask import Flask, render_template, request, jsonify
import pymysql
import json

app = Flask(__name__)

db = pymysql.connect(host = 'localhost',
                     port = 3306,
                     user = 'root',
                     passwd = 'Guswl1219',
                     db = 'mapaltofu',
                     charset = 'utf8')

cursor = db.cursor(pymysql.cursors.DictCursor)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/feed', methods=['GET'])
def get_feed():
    print('get_feed')
    title_receive = request.args.get('title_give')
    return jsonify({'result':'success', 'msg': '이 요청은 GET!'})
cursor.execute('select * from feed f;')
value = cursor.fetchall()
# print([value[0]])
db.commit()
db.close()

# # print([value[0]['title']])
# # # 마지막에 이게 꼭 나와야함


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)