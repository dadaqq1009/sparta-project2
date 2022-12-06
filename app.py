from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_bcrypt import Bcrypt
import pymysql, logging
import json

app = Flask(__name__)
app.secret_key = 'abcdefg'

# DEBUG -> INFO -> WARNING -> ERROR -> Critical
# # 파일로 남기기 위해서는 filename='test.log' 파라미터, 어느 로그까지 남길 것인지를 level 설정 가능하다.
# logging.basicConfig(filename='test.log', level=logging.ERROR)
#
# # 로그를 남길 부분에 다음과 같이 로그 레벨에 맞추어 출력해주면 해당 내용이 파일에 들어감
# # logging.debug("debug")
# # logging.info("info")
# # logging.warning("warning@@@@@@@@@@@@@@@@")
# logging.error("error############")
# logging.critical("critical$$$$$$$$$$$$")


# handler = logging.FileHandler('flask_error.log') # 메인파일 기준에서 상대경로 (절대경로로 해도 됨)
# handler.setLevel(logging.WARNING)  # ERROR 일때만 로깅하게 한다
# app.logger.addHandler(handler) # 핸들러 세팅

# 로그 생성
logger = logging.getLogger('loggin msg')

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler('my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

##################################
# bcrypt = Bcrypt(app)

##################################


# def connectSql():
#     db = pymysql.connect(host='localhost', port=3306, user='root',
#                          passwd='1234', db='mapaltofu', charset='utf8')
#     return db

db = pymysql.connect(host='localhost', port=3306, user='root',
                     passwd='1234', db='mapaltofu', charset='utf8')


@app.route('/')
def main():
    if 'login_id' in session:
        user_id = session['login_id']

        return render_template('main.html', logininfo=user_id)
    else:
        user_id = None
        return render_template('main.html', logininfo=user_id)


@app.route('/login_try')
def login_try():
    return render_template("login_try.html")


@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['login_id']
        user_pw = request.form['login_pw']

        cursor = db.cursor()

        sql = "SELECT * FROM user WHERE login_id = %s and pw = %s"
        value = (user_id, user_pw)

        cursor.execute(sql, value)
        data = cursor.fetchall()
        db.close()

        if data:
            session['login_id'] = user_id
            return render_template('main.html', logininfo=user_id)
        else:
            logger.info(f'login try fail..')
            return render_template('login_error.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('login_id', None)
    return redirect(url_for('main'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['register_id']
        user_pw = request.form['register_pw']
        user_name = request.form['register_name']
        user_email = request.form['register_email']

        cursor = db.cursor()

        sql = "select * from user where login_id = %s"
        value = user_id
        cursor.execute(sql, value)
        data = cursor.fetchall()

        if data:
            return render_template('register.html')
        else:
            sql = "insert into user (login_id, pw, name, email) values (%s,%s,%s,%s)"
            value = (user_id, user_pw, user_name, user_email)
            cursor.execute(sql, value)
            cursor.fetchall()

            db.commit()
            db.close()
            return render_template('main.html')
    else:
        return render_template('register.html')

@app.route('/user_edit', methods=['GET', 'POST'])
            # 회원정보 업데이트 공사중 입니다
def user_edit():
    if request.method == 'POST':
        if 'login_id' in session:
            login_id = session['login_id']

            edit_name = request.form['edit_name']
            edit_pw = request.form['edit_pw']
            edit_email = request.form['edit_email']

            cursor = db.cursor()
            sql = "update user set name = %s, pw = %s, email = %s"
            value = (edit_name, edit_pw, edit_email)
            cursor.execute(sql, value)

            session['login_id'] = login_id

            db.commit()
            db.close()
            return render_template('main.html', logininfo=login_id )
        else:
            return render_template('user_edit.html')
    else:
        return render_template('user_edit.html')



@app.route("/api/mypages", methods=['GET'])
def feed_get():
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

