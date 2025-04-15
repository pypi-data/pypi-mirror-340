from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RatmCls:
	"""Ratm commands group definition. 10 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ratm", core, parent)

	@property
	def grpNumber(self):
		"""grpNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_grpNumber'):
			from .GrpNumber import GrpNumberCls
			self._grpNumber = GrpNumberCls(self._core, self._cmd_group)
		return self._grpNumber

	@property
	def nresources(self):
		"""nresources commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nresources'):
			from .Nresources import NresourcesCls
			self._nresources = NresourcesCls(self._core, self._cmd_group)
		return self._nresources

	@property
	def rs(self):
		"""rs commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_rs'):
			from .Rs import RsCls
			self._rs = RsCls(self._core, self._cmd_group)
		return self._rs

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'RatmCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RatmCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
