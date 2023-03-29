from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from app.models import *
import googleTrends
import myplotly

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format('root', '19771201qwer',
# 'localhost','3306', 'new_or_novel')
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///../../db/flask.db'

db = SQLAlchemy(app)
CORS(app, supports_credentials=True)


@app.route('/tt')
def tt():
    return render_template('adduser.html')


@app.route('/')
def index():  # put application's code here
    s = db.session
    q = s.query(Byregion)
    return render_template('users.html', xx=q.all())


@app.route('/api/hotmap', methods=['GET', 'POST'])
def gethotmap():
    kw_list, timeframe_list, title = getmessage()
    df = googleTrends.services.getdatabyregion_overtime(kw_list, timeframe_list)
    fig = myplotly.hotmapbyword(df, title)
    return fig.to_json()


@app.route('/api/linechart', methods=['GET', 'POST'])
def getlinechart():
    kw_list, timeframe, title = getmessage()
    df = googleTrends.services.getdatabyovertime(kw_list, timeframe)
    fig = myplotly.linechart(df, title)
    return fig.to_json()


def getmessage():
    json_data = request.get_json()
    timeframe_list = json_data['timeframe_list']
    kw_list = json_data['kw_list']
    title = json_data['title']
    timeframe_list_c = []
    for timeframe in timeframe_list:
        timeframe_list_c.append(timeframe['start'] + ' ' + timeframe['end'])
    return kw_list, timeframe_list_c, title


@app.route('/api/kwlist', methods=['GET', 'POST'])
def getkwlist():
    result = None
    s = db.session
    if request.method == 'POST':
        json_data = request.get_json()
        pre_words = json_data['pre_words']
        result = [{"pre_words": row.pre_words, "post_words": row.post_words} for row in
                  s.query.filter_by(and_((WordList.pre_words == pre_word for pre_word in pre_words)))]
    elif request.method == 'GET':
        result = [{"pre_words": row.pre_words, "post_words": row.post_words} for row in s.query(WordList)]
    return result


if __name__ == '__main__':
    app.run()