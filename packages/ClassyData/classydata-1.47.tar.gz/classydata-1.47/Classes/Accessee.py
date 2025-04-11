#!/usr/bin/env python3

'''
Created on 12/01/2015

@author: dedson
'''

import sqlalchemy
import sqlalchemy.orm

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet

from .Base import Base

from .Visualisation import Visualisation
from .Accessor2Accessee import Accessor2Accessee

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object()
class Accessee(Visualisation):
	'''
	The Accessee class is used to define the access path as well as the list of accessors or users and groups that may access this class.
	'''

	__tablename__ = 'accessee'
	id            = Column(Integer, ForeignKey('visualisation.id'), primary_key=True)
	path          = Column(String(256))
	modifiers     = Column(String(256)) # enum of public, protected, private, static
	accessors     = relationship("Accessor", secondary='accessor2accessee', back_populates='accessees')

	__mapper_args__ = {
		'polymorphic_identity':'accessee'
	}

	def __init__(
		self,
		id=None,
		guid=None,
		inherited='accessee',
		version=None,
		fromDate=None,
		toDate=None,
		modified=None,
		display=None,
		robes=None,
		description=None,
		isLabel=None,
		path=None,
		modifiers=None,
		accessors=[]
	):
		super(Accessee,self).__init__(
			id=id,
			guid=guid,
			inherited=inherited,
			version=version,
			fromDate=fromDate,
			toDate=toDate,
			modified=modified,
			display=display,
			robes=robes,
			description=description,
			isLabel=isLabel
		)
		self.path = path
		self.modified = modified
		self.accessors = accessors
		return

	def __dir__(self):
		return Visualisation.__dir__(self) + [
			'path',
			'modifiers',
			'accessors',
		]

