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
    return json.dumps(value)

  def process_result_value(self, value, dialect):
    return json.loads(value)

mutable.MutableDict.associate_with(JsonEncodedDict)


BaseClass = declarative_base()

class XRole(BaseClass):
  __tablename__ = 'troles'
  id = sq.Column(sq.Integer, primary_key=True) 
  name = sq.Column(sq.String)
  foregin_name = sq.Column(sq.String)
  description = sq.Column(sq.String)
  source = sq.Column(sq.String)
  expire_at = sq.Column(sq.DateTime)
  user_id = sq.Column(sq.Integer, sq.ForeignKey('tusers.id'))
  user = relationship('XUser', back_populates='roles')

class XUser(BaseClass):
  __tablename__ = 'tusers'
  id = sq.Column(sq.Integer, primary_key=True)
  name = sq.Column(sq.String)
  attributes = sq.Column(JsonEncodedDict)
  tasks = relationship('XTask', back_populates='owner')
  processes = relationship('XProcess', back_populates='owner')
  roles = relationship('XRole', back_populates='user')

class XProcess(BaseClass):
  __tablename__ = 'tprocesses'
  id = sq.Column(sq.Integer, primary_key=True)
  owner_id = sq.Column(sq.Integer, sq.ForeignKey('tusers.id'))
  owner = relationship('XUser', back_populates='processes')
  conditions = relationship('XCondition', back_populates='process')
  tasks = relationship('XTask', back_populates='process')
  data = sq.Column(sq.String) 

class XCondition(BaseClass):
  __tablename__ = 'tconditions'
  id = sq.Column(sq.Integer, primary_key=True)
  process_id = sq.Column(sq.Integer, sq.ForeignKey('tprocesses.id'))
  process = relationship('XProcess', back_populates='conditions')
  tasks = relationship('XTask', back_populates='condition')
  module = sq.Column(sq.String)
  params = sq.Column(JsonEncodedDict)
  start_at = sq.Column(sq.DateTime)
  expire_at = sq.Column(sq.DateTime)
  done = sq.Column(sq.Boolean, default=False)

  
class XTask(BaseClass):
  __tablename__ = 'ttasks'
  id = sq.Column(sq.Integer, primary_key=True)
  params = sq.Column(sq.String)
  condition_id = sq.Column(sq.Integer, sq.ForeignKey('tconditions.id'))
  condition = relationship('XCondition', back_populates='tasks')
  process_id = sq.Column(sq.Integer, sq.ForeignKey('tprocesses.id'))
  process = relationship('XProcess', back_populates='tasks')
  owner_id = sq.Column(sq.Integer, sq.ForeignKey('tusers.id'))
  owner = relationship('XUser', back_populates='tasks')











