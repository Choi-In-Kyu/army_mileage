from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # def __repr__(self):
    #     return '<Task %r>' % self.user_id


@app.route('/', methods=['POST', 'GET'])
def index():
    # POST로 받은 값이 있을 때 (추가기능)
    # case getting POST (add)
    if request.method == 'POST':
        user_name = request.form['user_name']
        new_user = User(user_name=user_name)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an Issue Adding Your Task'
    # 일반 조회 페이지
    # default load page
    else:
        users = User.query.order_by(User.date_created).all()
        return render_template('index.html', users=users)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.route('/crawling', methods=['POST', 'GET'])
def crawling():
    response = urlopen('https://www.daum.net/')
    soup = BeautifulSoup(response, 'html.parser')
    result = ""
    for anchor in soup.select("a.link_favorsch"):
        result += str(anchor)
    # return result
    return render_template('crawling.html')


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delelte = User.query.get_or_404(id)

    try:
        db.session.delete(user_to_delelte)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':

        user.user_name = request.form['user_name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Fuck'
    else:
        return render_template('update.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)
