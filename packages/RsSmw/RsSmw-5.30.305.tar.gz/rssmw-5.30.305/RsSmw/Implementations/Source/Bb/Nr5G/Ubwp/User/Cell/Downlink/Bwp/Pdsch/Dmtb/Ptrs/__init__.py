from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PtrsCls:
	"""Ptrs commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ptrs", core, parent)

	@property
	def epre(self):
		"""epre commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_epre'):
			from .Epre import EpreCls
			self._epre = EpreCls(self._core, self._cmd_group)
		return self._epre

	@property
	def mcs1(self):
		"""mcs1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs1'):
			from .Mcs1 import Mcs1Cls
			self._mcs1 = Mcs1Cls(self._core, self._cmd_group)
		return self._mcs1

	@property
	def mcs2(self):
		"""mcs2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs2'):
			from .Mcs2 import Mcs2Cls
			self._mcs2 = Mcs2Cls(self._core, self._cmd_group)
		return self._mcs2

	@property
	def mcs3(self):
		"""mcs3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs3'):
			from .Mcs3 import Mcs3Cls
			self._mcs3 = Mcs3Cls(self._core, self._cmd_group)
		return self._mcs3

	@property
	def rb0(self):
		"""rb0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rb0'):
			from .Rb0 import Rb0Cls
			self._rb0 = Rb0Cls(self._core, self._cmd_group)
		return self._rb0

	@property
	def rb1(self):
		"""rb1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rb1'):
			from .Rb1 import Rb1Cls
			self._rb1 = Rb1Cls(self._core, self._cmd_group)
		return self._rb1

	@property
	def reof(self):
		"""reof commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reof'):
			from .Reof import ReofCls
			self._reof = ReofCls(self._core, self._cmd_group)
		return self._reof

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'PtrsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PtrsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
