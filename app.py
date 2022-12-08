from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql, logging, json, uuid, os
import bcrypt

try:
    from werkzeug.utils import secure_filename
except:
    from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = 'abcdefg'


db = pymysql.connect(host = 'localhost',
                     port = 3306,
                     user = 'root',
                     passwd = 'Guswl1219',
                     db = 'mapaltofu',
                     charset = 'utf8')
# db = SQLAlchemy(app)

# cursor = db.cursor(pymysql.cursors.DictCursor)
cursor = db.cursor()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #파일 업로드 용량 제한 단위:바이트 (현재 16메가 세팅)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Guswl1219@localhost:3306/mapaltofu"
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

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

##################################

@app.route('/')
def main():
    if 'login_id' in session:
        user_id = session['login_id']
        login_name = session['login_name']

        return render_template('main.html', logininfo=user_id, loginName=login_name)
    else:
        user_id = None
        return render_template('main.html', logininfo=user_id)


@app.route('/login_try')
def login_try():
    return render_template("login_try.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['login_id']
        user_pw = request.form['login_pw']

        cursor = db.cursor()
        sql = "SELECT * FROM `user` where login_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchall()

        for row in data:
            db_pw = row[3]
            login_name = row[2]
            print(row)

        if data:
            if bcrypt.checkpw(user_pw.encode('utf-8'), db_pw.encode('utf-8')):
                session['login_id'] = user_id
                session['login_name'] = login_name
                return render_template('main.html', logininfo=user_id, loginName=login_name)

            else:
                logger.info(f'login try fail..')
                return render_template('login_error.html')
        else:
            logger.info(f'login try fail..')
            return render_template('login_error.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['register_id']

        user_pw = request.form['register_pw']
        input_bcrypt = bcrypt.hashpw(user_pw.encode('utf-8'), bcrypt.gensalt())
        input_decode = input_bcrypt.decode('utf-8')

        user_name = request.form['register_name']
        user_email = request.form['register_email']

        cursor = db.cursor()

        sql = "select * from `user` where login_id = %s and email = %s"
        value = (user_id, user_email)
        cursor.execute(sql, value)
        data = (cursor.fetchall())

        if data:
            logger.info(f'sigin try fail..')
            return render_template('register.html')
        else:
            sql = "insert into `user` (login_id, pw, name, email) values (%s,%s,%s,%s)"
            value = (user_id, input_decode, user_name, user_email)
            cursor.execute(sql, value)
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
            input_bcrypt = bcrypt.hashpw(edit_pw.encode('utf-8'), bcrypt.gensalt())
            input_decode = input_bcrypt.decode('utf-8')

            edit_email = request.form['edit_email']

            cursor = db.cursor()
            sql = "update `user` set name = %s, pw = %s, email = %s where login_id = %s"
            value = (edit_name, input_decode, edit_email, login_id)

            cursor.execute(sql, value)

            session['login_id'] = login_id

            db.commit()
            # db.close()
            return render_template('edit_success.html', logininfo=login_id )
        else:
            logger.info(f'user_edit fail..')
            return render_template('login_error.html')
    else:
        return render_template('user_edit.html')


@app.route('/mypage')
def mypage():
    if 'login_id' in session:
        user_id = session['login_id']
        login_name = session['login_name']
        return render_template('mypage.html', logininfo=user_id, loginName=login_name)

@app.route("/api/mypage", methods=['GET'])
def mypages():
    if request.method == "GET":
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
        # db.close()
        return json_str, 200


@app.route('/edit_success')
def edit_success():
    return render_template('edit_success.html')



@app.route("/modify")
def modify_feed():
    if 'login_id' in session:
        user_id = session['login_id']
        login_name = session['login_name']
        return render_template('modify.html', logininfo=user_id, loginName=login_name)

@app.route("/api/modify", methods=['POST'])
def edit_feed():
    if request.method == "POST":
        feed_id = request.form['id']
        title = request.form['title']
        description = request.form['description']

        sql = """
                    UPDATE feed
                    SET title = %s,
                     description = %s
                     WHERE id = %s;
                    """

        value = (title, description, feed_id)

        cursor.execute(sql, value)

        db.commit()

        return json.dumps('post modified successfully!')


@app.route('/feed_page')
def feed_pages():
    if 'login_id' in session:
        user_id = session['login_id']
        return render_template('feed_page.html', logininfo = user_id)
    else:
        return render_template('feed_page.html')

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

@app.route("/api/delete", methods=['POST'])
def delete_feed():
    if request.method == "POST":
        feed_id = request.form['id']
        sql = """
                       DELETE FROM feed WHERE id = %s;
                                   """

        value = feed_id
        cursor.execute(sql, value)

        db.commit()

        return json.dumps('post deleted successfully!')

@app.route('/write_success')
def write_success():
    if'login_id' in session:
        user_id = session['login_id']
        return render_template('write_success.html', logininfo=user_id)

# def render_picture(data):
#
#     render_pic = base64.b64encode(data).decode('ascii')
#     return render_pic

@app.route('/write', methods=['GET','POST'])
def write():
    if request.method == 'POST':
        if 'login_name' in session:
            title = request.form['title']
            description = request.form['description']
            file = request.files['file']
            file.save('./static/images/' + secure_filename(file.filename))
            image = './static/images/' + file.filename
            sql = "insert into feed(title, description, image) values (%s, %s, %s)"
            value = (title, description, image)
            cursor.execute(sql, value)
            db.commit()

            return redirect(url_for('write_success'))
        else:
            return render_template('login_error.html')
    else:
        if 'login_name' in session:
            login_id = session['login_id']
            login_name = session['login_name']
            return render_template('write.html', logininfo=login_id, loginName=login_name)
        else:
            return render_template('main.html')


# 파일 리스트
# @app.route('/list')
# def list_page():
#     file_list = os.listdir("./uploads")
#     html = """<center><a href="/">홈페이지</a><br><br>"""
#     html += "file_list: {}".format(file_list) + "</center>"
#     return html


# 업로드 HTML 렌더링
@app.route('/upload')
def upload_page():
    return render_template('upload.html')


# 파일 업로드 처리
@app.route('/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # hash_value = uuid.uuid4().hex
        # 저장할 경로 + 파일명
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'], hash_value + secure_filename(f.filename)))
        f.save('./static/images/' + secure_filename(f.filename))
        return redirect(url_for('mypage'))



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


