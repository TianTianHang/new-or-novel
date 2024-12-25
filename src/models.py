# 用户和角色之间是多对多关系，需要创建关联表来表示这种关系
from extendsions import db

user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                     )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # 定义多对多关系，一个用户可以有多个角色
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(80), unique=True, nullable=False)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_category = db.Column(db.String(50), nullable=False)
    word_text = db.Column(db.String(100), nullable=False)
    word_details = db.Column(db.Text, nullable=True)

    __table_args__ = (db.UniqueConstraint('word_text', 'word_category', name='_word_text_category_uc'),)
