from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ArrivalCls:
	"""Arrival commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("arrival", core, parent)

	@property
	def angle(self):
		"""angle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_angle'):
			from .Angle import AngleCls
			self._angle = AngleCls(self._core, self._cmd_group)
		return self._angle

	@property
	def spread(self):
		"""spread commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spread'):
			from .Spread import SpreadCls
			self._spread = SpreadCls(self._core, self._cmd_group)
		return self._spread

	def clone(self) -> 'ArrivalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ArrivalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
