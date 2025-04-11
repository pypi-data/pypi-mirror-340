#!/usr/bin/env python3

'''
Created on 12/01/2015

@author: dedson
'''

import sqlalchemy
import sqlalchemy.orm

from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet

from .Base import Base
from .Permission import Permission

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object()
class Accessor2Accessee(Base):

	__tablename__ = 'accessor2accessee'
	accessor_id = Column(Integer, ForeignKey('accessor.id'), primary_key=True)
	accessee_id = Column(Integer, ForeignKey('accessee.id'), primary_key=True)
	permissions = Column(Integer) # bitmap of Permission OR together

	def __init__(
		self,
		accessor_id=None,
		accessee_id=None,
		permissions=None
	):
		self.accessor_id = accessor_id
		self.accessee_id = accessee_id
		self.permissions = permissions

	def __dir__(self):
		return [
			'accessor_id',
			'accessee_id',
			'permissions'
		]

