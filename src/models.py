# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()
Base = db.Model
metadata = Base.metadata


class Byovertime(Base):
    __tablename__ = 'byovertime'

    time = Column(String(100), primary_key=True, nullable=False)
    word = Column(String(100), primary_key=True, nullable=False)
    HeatValue = Column(Integer, nullable=False)


class Byregion(Base):
    __tablename__ = 'byregion'

    geoCode = Column(String(100), primary_key=True, nullable=False)
    geoName = Column(String(100), nullable=False)
    time = Column(String(100), primary_key=True, nullable=False)
    word = Column(String(100), primary_key=True, nullable=False)
    HeatValue = Column(Integer, nullable=False)


class WordList(Base):
    __tablename__ = 'wordList'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    pre_words = Column(String(100), nullable=False)
    post_words = Column(String(100), nullable=True)
    title = Column(String(100), nullable=True)
    content = Column(String(100), nullable=True)
    parent_id = Column(Integer, ForeignKey('wordList.id'), nullable=True)
    has_hover = Column(Boolean, nullable=False)
    children = relationship("WordList", backref=backref("parent", remote_side=[id]))
