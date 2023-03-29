# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
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
    pre_words = Column(String(100), primary_key=True, nullable=False)

    post_words = Column(String(100), primary_key=True, nullable=False)
