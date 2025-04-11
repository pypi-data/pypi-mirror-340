#!/usr/bin/env python3

from enum import IntEnum

class Permission(IntEnum):

	Create = 1
	Read = 2
	Update = 4
	Delete = 8
	Execute = 16
	Manage = 32
