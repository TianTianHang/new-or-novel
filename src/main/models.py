from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, Text, Table

from sqlalchemy.orm import relationship

from main.database import Base

user_role = Table("user_role", Base.metadata,
                  Column("user_id", Integer, ForeignKey('user.id'), primary_key=True),
                  Column("role_id", Integer, ForeignKey('role.id'), primary_key=True))


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    hashed_password = Column(String(120), nullable=False)
    email = Column(String(80), nullable=True)
    # 定义多对多关系，一个用户可以有多个角色
    roles = relationship('Role', secondary=user_role, back_populates="users")


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    role_name = Column(String(80), unique=True, nullable=False)
    users = relationship("User", secondary=user_role, back_populates="roles")


class Word(Base):
    __tablename__ = "word"
    id = Column(Integer, primary_key=True)
    word_category = Column(String(50), nullable=False)
    word_text = Column(String(100), nullable=False)
    word_details = Column(Text, nullable=True)

    __table_args__ = (UniqueConstraint('word_text', 'word_category', name='_word_text_category_uc'),)
