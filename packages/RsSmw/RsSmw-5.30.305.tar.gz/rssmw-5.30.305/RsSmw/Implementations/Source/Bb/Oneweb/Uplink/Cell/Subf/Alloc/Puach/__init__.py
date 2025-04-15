from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PuachCls:
	"""Puach commands group definition. 16 total commands, 9 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("puach", core, parent)

	@property
	def codewords(self):
		"""codewords commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_codewords'):
			from .Codewords import CodewordsCls
			self._codewords = CodewordsCls(self._core, self._cmd_group)
		return self._codewords

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Conflict import ConflictCls
			self._conflict = ConflictCls(self._core, self._cmd_group)
		return self._conflict

	@property
	def cqi(self):
		"""cqi commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_cqi'):
			from .Cqi import CqiCls
			self._cqi = CqiCls(self._core, self._cmd_group)
		return self._cqi

	@property
	def drs(self):
		"""drs commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_drs'):
			from .Drs import DrsCls
			self._drs = DrsCls(self._core, self._cmd_group)
		return self._drs

	@property
	def harq(self):
		"""harq commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Harq import HarqCls
			self._harq = HarqCls(self._core, self._cmd_group)
		return self._harq

	@property
	def ndmrs(self):
		"""ndmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndmrs'):
			from .Ndmrs import NdmrsCls
			self._ndmrs = NdmrsCls(self._core, self._cmd_group)
		return self._ndmrs

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def set(self):
		"""set commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_set'):
			from .Set import SetCls
			self._set = SetCls(self._core, self._cmd_group)
		return self._set

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'PuachCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PuachCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
