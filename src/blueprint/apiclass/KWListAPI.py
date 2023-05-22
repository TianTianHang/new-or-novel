from flask import jsonify
from flask.views import MethodView

from models import db
from utils.helper import get_tree, get_kw_by_id


class KWListAPI(MethodView):

    def get(self, kw_id=None):
        if kw_id is None:
            # 返回一个包含所有单词的树
            result, nextId = get_tree(db)
            return jsonify(dict(tree=result, nextId=nextId))
        else:
            # 返回一个单词信息
            result = get_kw_by_id(db, kw_id)
            return jsonify(result)

    def post(self):
        # 添加一个单词
        pass

    def delete(self, user_id):
        # 删除一个单词
        pass

    def put(self, user_id):
        # 更新一个单词
        pass
