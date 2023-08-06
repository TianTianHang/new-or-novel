from flask_restful import Resource, reqparse

from extendsions import db
from models import Word

# Request parser for word creation
word_parser = reqparse.RequestParser()
word_parser.add_argument('word_text', type=str, required=True, help='Word text is required')
word_parser.add_argument('word_category', type=str, required=True, help='Word category is required')
word_parser.add_argument('word_details', type=str, help='Word details should be a string')


class WordResource(Resource):
    def get(self, word_id):
        word = Word.query.get(word_id)
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
        }

    def post(self):
        args = word_parser.parse_args(strict=True)

        word_text = args['word_text']
        word_category = args['word_category']
        word_details = args['word_details']

        word = Word(word_text=word_text, word_category=word_category, word_details=word_details)

        db.session.add(word)
        db.session.commit()
        return {"code": 200, "data": {"id": word.id}, "message": "Word created successfully"}, 200
