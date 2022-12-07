from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
# from flask_bcrypt import Bcrypt
import pymysql, logging, json

app = Flask(__name__)
app.secret_key = 'abcdefg'

db = pymysql.connect(host = 'localhost',
                     port = 3306,
                     user = 'root',
                     passwd = '1234',
                     db = 'mapaltofu',
                     charset = 'utf8')

# cursor = db.cursor(pymysql.cursors.DictCursor)
cursor = db.cursor()

@app.route('/feed', methods=['GET'])
def get_feed():
    sql = """
    select * from feed as f left join `user` as u on f.user_id = u.id
    """
    cursor.execute(sql)
    rows = cursor.fetchall() # 피드에있는 데이터를 다 가져온다
    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str) # json포맷으로 변환
    db.commit()
    return json_str, 200


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
bcrypt = Bcrypt(app)
##################################

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


@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['login_id']
        user_pw = request.form['login_pw']

        cursor = db.cursor()

        sql = "SELECT * FROM `user` WHERE login_id = %s and pw = %s"
        value = (user_id, user_pw)

        cursor.execute(sql, value)
        data = cursor.fetchall()

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

        sql = "select * from `user` where login_id = %s or email = %s"
        value = (user_id, user_email)
        cursor.execute(sql, value)
        data = (cursor.fetchall())



        if data:
            return render_template('login_error.html')
        else:
            sql = "insert into `user` (login_id, pw, name, email) values (%s,%s,%s,%s)"
            value = (user_id, user_pw, user_name, user_email)
            cursor.execute(sql, value)
            # bcrypt.generate_password_hash(user_pw)
            cursor.fetchall()
            db.commit()
            # db.close()
            return render_template('main.html')
    else:
        return render_template('register.html')

@app.route('/user_edit', methods=['GET', 'POST'])
def user_edit():
    if request.method == 'POST':
        if 'login_id' in session:
            login_id = session['login_id']

            edit_name = request.form['edit_name']
            edit_pw = request.form['edit_pw']
            edit_email = request.form['edit_email']

            cursor = db.cursor()
            sql = "update `user` set name = %s, pw = %s, email = %s where login_id = %s"
            value = (edit_name, edit_pw, edit_email, login_id)

            # sql = "update `user` set name = %s, pw = %s, email = %s"
            # value = (edit_name, edit_pw, edit_email)
            cursor.execute(sql, value)

            session['login_id'] = login_id

            db.commit()
            # db.close()
            return render_template('edit_success.html', logininfo=login_id )
        else:
            return render_template('login_error.html')
    else:
        return render_template('user_edit.html')


@app.route('/<login_id>')
def mypages():
    if 'login_id' in session:
        user_id = session['login_id']
        return render_template('mypage.html', logininfo = user_id)

@app.route("/<login_id>", methods=['GET'])
def mypage(login_id):
     # 여기 foreign key 방식으로 다시 써야됨!!!!
     sql = """
     select *
     from feed as f
     LEFT JOIN `user` as u
     ON f.user_id = u.id
     """
     cursor.execute(sql)
     rows = cursor.fetchall()


     json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
     db.commit()
     # db.close()
     return json_str, 200

@app.route('/edit_success')
def edit_success():
    return render_template('edit_success.html')


@app.route("/api/mypages", methods=['GET'])
def feed_get():
    # curs = db.cursor()
    # 여기 foreign key 방식으로 다시 써야됨!!!!

    sql = """
    select * 
    from feed as f
    LEFT JOIN `user` as u
    ON f.user_id = u.id
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
    db.commit()
    return json_str, 200


# @app.route("/api/mypages", methods=['GET'])
# def feed_get():
#     # curs = db.cursor()
#
#     # 여기 foreign key 방식으로 다시 써야됨!!!!
#     sql = """
#     select *
#     from feed as f
#     LEFT JOIN `user` as u
#     ON f.user_id = u.id
#     """
#     cursor.execute(sql)
#     rows = cursor.fetchall()
#
#
#     json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
#     db.commit()
#     # db.close()
#     return json_str, 200

@app.route('/feed_page')
def feed_pages():
    if 'login_id' in session:
        user_id = session['login_id']
        return render_template('feed_page.html', logininfo = user_id)

@app.route("/feed_page/<login_id>/<id>", methods=["GET"])
def feed_page(login_id, id):

    sql = """
    select * 
    from feed as f
    LEFT JOIN `user` as u
    ON f.user_id = u.id
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
    db.commit()
    return json_str, 200



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


