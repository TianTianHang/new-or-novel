
import pandas as pd
from flask import Flask, request
from flask_cors import CORS
from flask import render_template
from sqlalchemy import and_
from sqlalchemy import event

from googleTrends.services import getDataByRegionAndOvertime, getDataOvertimeMultiWord
from myplotly import hotmapbyword,linechart
from utils.helper import get_tree, getmessage
from utils import config
from utils.models import WordList, db

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format('root', '19771201qwer',
# 'localhost','3306', 'new_or_novel')
app.config.from_object(config)

db.init_app(app)
with app.app_context():
    db.create_all()

CORS(app, supports_credentials=True, max_age=2592000)


@event.listens_for(WordList.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    s = db.session
    s.add(WordList(pre_words="new", has_hover=False))
    s.add(WordList(pre_words="novel", has_hover=False))
    s.commit()


@app.route('/api/hotmap', methods=['GET', 'POST'])
def gethotmap():
    kw_list, timeframe_list, title = getmessage(request)
    df = getDataByRegionAndOvertime(kw_list, timeframe_list)
    df['HeatValue'] = df.iloc[..., 5:].sum(axis=1)
    fig = hotmapbyword(df, title)
    return fig.to_json()


@app.route('/api/linechart', methods=['GET', 'POST'])
def getlinechart():
    kw_list, timeframe, title = getmessage(request)
    df: pd.DataFrame = getDataOvertimeMultiWord(kw_list, timeframe)
    df['HeatValue'] = df.iloc[..., 2:].sum(axis=1)
    df = df.melt(id_vars='time', var_name='word', value_name='value')
    fig = linechart(df, title)
    return fig.to_json()


@app.route('/api/kwlist', methods=['GET', 'POST'])
def getkwlist():
    result, nextId = get_tree(db)
    return dict(tree=result, nextId=nextId)


@app.route('/addWord', methods=['GET', 'POST'])
def addWord():
    word_tree = get_tree(db)
    return render_template("word_form.html", wordsTree=word_tree)


# 插入批量插入单词
@app.route('/add', methods=['GET', 'POST'])
def add():
    df = pd.read_json("top10-new-live.json")
    s = db.session
    root = s.query(WordList).filter(and_(WordList.parent_id == None, WordList.pre_words == "new")).all()
    for word in df.index:
        s.add(WordList(pre_words='new', post_words=str(word).lower(), parent_id=root[0].id, has_hover=False))
    s.commit()
    return None


if __name__ == '__main__':
    app.run()
