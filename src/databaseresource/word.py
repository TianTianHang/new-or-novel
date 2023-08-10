from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from extendsions import db
from models import Word

# Request parser for word creation
word_parser = reqparse.RequestParser()
word_parser.add_argument('word_text', type=str, required=True, help='Word text is required')
word_parser.add_argument('word_category', type=str, required=True, help='Word category is required')
word_parser.add_argument('word_details', type=str, help='Word details should be a string')


class WordResource(Resource):
    @jwt_required()
    def get(self, word_id_or_text):
        word = None

        if word_id_or_text.isdigit():
            # If word_id_or_text is a number, treat it as word_id
            word = Word.query.get(word_id_or_text)
        else:
            # If word_id_or_text is not a number, treat it as word_text and perform text-based search
            word = Word.query.filter_by(word_text=word_id_or_text).first()

        if not word:
            return {"code": 404, "data": None, "message": "Word not found"}, 404

        return {
            "code": 200,
            "data": {
                "id": word.id,
                "word_text": word.word_text,
                "word_category": word.word_category,
                "word_details": word.word_details
            },
            "message": "Success"
        }, 200

    @jwt_required()
    def post(self):
        args = word_parser.parse_args(strict=True)

        word_text = args['word_text']
        word_category = args['word_category']
        word_details = args['word_details']

        word = Word(word_text=word_text, word_category=word_category, word_details=word_details)

        db.session.add(word)
        db.session.commit()
        return {"code": 200, "data": {"id": word.id}, "message": "Word created successfully"}, 200

    @jwt_required()
    def put(self, word_id):
        word = Word.query.get(word_id)
        if not word:
            return {"code": 404, "data": None, "message": "Word not found"}, 404

        args = word_parser.parse_args(strict=True)

        word.word_text = args['word_text']
        word.word_category = args['word_category']
        word.word_details = args['word_details']

        db.session.commit()
        return {
            "code": 200,
            "data": None,
            "message": "Word updated successfully"
        }, 200

    @jwt_required()
    def delete(self, word_id):
        word = Word.query.get(word_id)
        if not word:
            return {"code": 404, "data": None, "message": "Word not found"}, 404

        db.session.delete(word)
        db.session.commit()
        return {"code": 200, "data": None, "message": "Word deleted successfully"}, 200


class WordListResource(Resource):
    @jwt_required()
    def get(self):
        category = request.args.get('category', None)
        words = Word.query.all()
        word_list = []

        for word in words:
            if category and word.word_category != category:
                continue

            word_data = {
                "id": word.id,
                "word_category": word.word_category,
                "word_text": word.word_text,
                "word_details": word.word_details
            }
            word_list.append(word_data)

        return {'code': 200, 'data': word_list, 'message': 'Success'}, 200
