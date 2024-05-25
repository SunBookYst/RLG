'''
数据库模型.
'''
from flask import SQLAlchemy

db = SQLAlchemy()

# 数据模型
class User(db.Model):
    # TODO