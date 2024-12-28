# 用户和角色之间是多对多关系，需要创建关联表来表示这种关系
import datetime
import json
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
    
    
    
class Cache(db.Model):
    __tablename__ = 'cache'

    id = db.Column(db.Integer, primary_key=True)
    func_name = db.Column(db.String(255), nullable=False)
    params = db.Column(db.Text, nullable=False)  # 可以存储JSON字符串
    result = db.Column(db.Text, nullable=False)  # 存储JSON或其他格式的结果
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<Cache(id={self.id}, func_name={self.func_name}, created_at={self.created_at})>"

    def serialize(self):
        """将对象转换为字典形式"""
        return {
            'id': self.id,
            'func_name': self.func_name,
            'params': json.loads(self.params),
            'result': json.loads(self.result),
            'created_at': self.created_at,
        }

    @staticmethod
    def to_dict(cache_obj):
        """辅助方法用于转换缓存记录为字典格式"""
        return {
            'id': cache_obj.id,
            'func_name': cache_obj.func_name,
            'params': json.loads(cache_obj.params),
            'result': json.loads(cache_obj.result),
            'created_at': cache_obj.created_at,
        }