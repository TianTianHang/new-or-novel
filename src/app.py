import pandas as pd
from flask import Flask, request
from flask_cors import CORS
from flask import render_template
from sqlalchemy import and_
from sqlalchemy import event

from blueprint import kwlist_bp, heatmap_bp, line_chart_bp
from googleTrends.services import getDataByRegionAndOvertime, getDataOvertimeMultiWord
from myplotly import density_mapbyword, linechart
from utils.helper import get_tree, getmapsource
import config
from models import WordList, db

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format('root', '19771201qwer',
# 'localhost','3306', 'new_or_novel')
app.config.from_object(config)

db.init_app(app)
with app.app_context():
    db.create_all()

CORS(app, supports_credentials=True, max_age=2592000)
sources = getmapsource()


@event.listens_for(WordList.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    s = db.session
    s.add(WordList(pre_words="new", has_hover=False))
    s.add(WordList(pre_words="novel", has_hover=False))
    s.commit()


@app.route('/')
def index():
    return "yes!"


app.register_blueprint(line_chart_bp)
app.register_blueprint(heatmap_bp)
app.register_blueprint(kwlist_bp)


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
