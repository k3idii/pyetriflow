from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy as sq
from sqlalchemy.types import TypeDecorator, VARCHAR
import json

from sqlalchemy.ext import mutable

class JsonEncodedDict(sq.TypeDecorator):
  """Enables JSON storage by encoding and decoding on the fly."""
  impl = sq.String

  def process_bind_param(self, value, dialect):
    return simplejson.dumps(value)

  def process_result_value(self, value, dialect):
    return simplejson.loads(value)

mutable.MutableDict.associate_with(JsonEncodedDict)


BaseClass = declarative_base()

class XRole(BaseClass):
  __tablename__ = 'roles'
  id = sq.Column(sq.Integer, primary_key=True) 
  name = sq.Column(sq.String)
  foregin_name = sq.Column(sq.String)
  description = sq.Column(sq.String)
  source = sq.Column(sq.String)
  expire_at = sq.Column(sq.DateTime)
  user_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'))
  user = relationship('XUser', back_populates='roles')

class XUser(BaseClass):
  __tablename__ = 'users'
  id = sq.Column(sq.Integer, primary_key=True)
  name = sq.Column(sq.String)
  attributes = sq.Column(JsonEncodedDict)
  tasks = relationship('XTask', back_populates='users')
  processes = relationship('XProcess', back_populates='users')
  roles = relationship('XRole', back_populates='users')

class XProcess(BaseClass):
  __tablename__ = 'processes'
  id = sq.Column(sq.Integer, primary_key=True)
  owner_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'))
  owner = relationship('XUser', back_populates='processes')
  conditions = relationship('XCondition', back_populates='processes')
  data = sq.Column(sq.String) 

class XCondition(BaseClass):
  __tablename__ = 'conditions'
  id = sq.Column(sq.Integer, primary_key=True)
  process_is = sq.Column(sq.Integer, sq.ForeignKey('processes.id'))
  process = relationship('XProcess', back_populates='conditions')
  module = sq.Column(sq.String)
  params = sq.Column(JsonEncodedDict)
  start_at = sq.Column(sq.DateTime)
  expire_at = sq.Column(sq.DateTime)
  done = sq.Column(sq.Boolean, default=False)

  
class XTask(BaseClass):
  __tablename__ = 'tasks'
  id = sq.Column(sq.Integer, primary_key=True)
  params = sq.Column(sq.String)
  condition_id = sq.Column(sq.Integer, sq.ForeignKey('conditions.id'))
  condition = relationship('XCondition', back_populates='tasks')
  process_is = sq.Column(sq.Integer, sq.ForeignKey('processes.id'))
  process = relationship('XProcess', back_populates='tasks')
  owner_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'))
  owner = relationship('XUser', back_populates='tasks')











