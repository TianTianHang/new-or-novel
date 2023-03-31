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
    nodes = None
    s = db.session
    if request.method == 'POST':
        json_data = request.get_json()
        pre_words = json_data['pre_words']
        nodes = get_nodes(s.query.filter_by(and_((WordList.pre_words == pre_word for pre_word in pre_words))))
    elif request.method == 'GET':
        # 取出数据构造成字典
        nodes = get_nodes(s.query(WordList).order_by("pre_words"))

    # 根据child_id构造嵌套字典
    result = build_tree(nodes)
    return result


# s是数据库会话
def get_nodes(query_result):
    nodes = [{
        "id": row.id,
        "word": {"pre_words": row.pre_words, "post_words": row.post_words},
        "title": row.title,
        "img": row.img,
        "content": row.content,
        "parent_id": row.parent_id
    } for row in query_result]
    return nodes


def build_tree(nodes, parent_id=None):
    tree = []
    for node in nodes:
        if node['parent_id'] == parent_id:
            children = build_tree(nodes, node['id'])
            if children:
                node['children'] = [{k: v for k, v in child.items() if k not in ['id', 'parent_id']} for child in children]
            tree.append({k: v for k, v in node.items() if k not in ['id', 'parent_id']})
    return tree


if __name__ == '__main__':
    app.run()
