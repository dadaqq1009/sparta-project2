from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests


@app.route('/')
def mypage():
    return render_template('mypage.html')


@app.route("/mypage", methods=["GET"])
def feed_get():
    return jsonify({'msg': '완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

