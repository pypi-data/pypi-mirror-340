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
from .Accessee import Accessee

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object(suppress=['parent'])
class Instance(Accessee):
	'''
	this represents an object instance of a particular class and version
	'''

	__tablename__ = 'instance'

	id           = Column(Integer, ForeignKey('accessee.id'), primary_key=True)
	name         = Column(String(256)) # is name of attribute if for a fundamental
	value        = Column(String(256)) # only for fundamental types
	is_list      = Column(Boolean())
	attribute_id = Column(Integer, ForeignKey('attribute.id'))
	attribute    = relationship("Attribute", uselist=False, foreign_keys=[attribute_id])
	clasz_id     = Column(Integer, ForeignKey('class.id'))
	clasz        = relationship('Class', uselist=False, foreign_keys=[clasz_id])
	parent_id    = Column(Integer, ForeignKey('instance.id'))
	parent	     = relationship("Instance", uselist=False, foreign_keys=[parent_id], remote_side=[id])

	__mapper_args__ = {
		'polymorphic_identity':'instance'
	}

	def __init__(
		self,
		id=None,
		guid=None,
		inherited='instance',
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
		attribute=None,
		attribute_id=None,
   		clasz=None,
		clasz_id=None,
		is_list=False,
		name=None,
		value=None,
		parent_id=None,
		parent=None
	):
		super(Instance,self).__init__(
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
			isLabel=isLabel,
			path=path,
			modifiers=modifiers
		)
		self.name = name
		self.value = value
		self.is_list = is_list
		self.attribute_id = attribute_id
		if attribute:
			self.attribute = attribute
			self.attribute_id = attribute.id
		self.clasz_id = clasz_id
		if clasz:
			self.clasz = clasz
			self.clasz_id = clasz.id
		self.parent_id = parent_id
		if parent:
			self.parent = parent
			self.parent_id = parent.id
		return

	def __dir__(self):
		return Accessee.__dir__(self) + [
			'id',
			'name',
			'value',
			'is_list',
			'parent_id',
			'attribute_id',
			'attribute',
			'clasz_id',
			'clasz'
		]


