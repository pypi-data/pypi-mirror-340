#!/usr/bin/env python3

'''
Created on 12/01/2015

@author: dedson
'''

import sqlalchemy
import sqlalchemy.orm

from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet

from .Base import Base

class User2Group(Base):

	__tablename__ = 'user2group'
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)


