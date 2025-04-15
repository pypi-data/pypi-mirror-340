from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeCls:
	"""Time commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	@property
	def premp(self):
		"""premp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_premp'):
			from .Premp import PrempCls
			self._premp = PrempCls(self._core, self._cmd_group)
		return self._premp

	@property
	def prepre(self):
		"""prepre commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prepre'):
			from .Prepre import PrepreCls
			self._prepre = PrepreCls(self._core, self._cmd_group)
		return self._prepre

	def clone(self) -> 'TimeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TimeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
