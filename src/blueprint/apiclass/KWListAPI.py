from flask import jsonify, request
from flask.views import MethodView
from marshmallow import Schema, fields

from models import db
from utils.helper import get_tree, get_kw_by_id, add_kw, update_kw, remove_kw


class KeyWordMoreInfoSchema(Schema):
    id = fields.Integer(required=False, allow_none=True, description='id')
    word = fields.Nested(
        lambda: KeyWordSchema(),
        required=False,
        allow_none=True,
        description='Word information'
    )
    title = fields.String(required=False, allow_none=True, description='Title')
    content = fields.String(required=False, allow_none=True, description='Content')
    has_hover = fields.Boolean(required=True, description='Has Hover')
    parent_id = fields.Integer(required=True, allow_none=True, description='parent_id')


class KeyWordSchema(Schema):
    pre_words = fields.String(required=True, description='Pre Words')
    post_words = fields.String(required=False, allow_none=True, description='Post Words')


class KWListAPI(MethodView):

    def get(self, kw_id=None):
        if kw_id is None:
            # 返回一个包含所有单词的树
            result = get_tree(db)
            return jsonify(dict(tree=result))
        else:
            # 返回一个单词信息
            result = get_kw_by_id(db, kw_id)
            return jsonify(result)

    def post(self):
        # 添加一个单词
        (validate, data, cord) = self.valid_message(request)
        if validate:
            kw_id = add_kw(db, data)
            return jsonify(dict(id=kw_id)), cord
        else:
            return jsonify(data), cord

    def delete(self, kw_id):
        # 删除一个单词
        rs = remove_kw(db, kw_id)
        print(rs)
        return jsonify(dict(n=rs)), 200

    def put(self):
        # 更新一个单词
        (validate, data, cord) = self.valid_message(request)
        if validate:
            rs = update_kw(db, data)
            print(rs)
            return jsonify(dict(n=rs)), cord
        else:
            return jsonify(data), cord

    def valid_message(self, request):
        schema = KeyWordMoreInfoSchema()
        form = request.get_json()
        result = schema.validate(form)
        if result:
            return False, result, 400
        else:
            return True, form, 200
