from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GlonassCls:
	"""Glonass commands group definition. 8 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("glonass", core, parent)

	@property
	def utcsu(self):
		"""utcsu commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_utcsu'):
			from .Utcsu import UtcsuCls
			self._utcsu = UtcsuCls(self._core, self._cmd_group)
		return self._utcsu

	def clone(self) -> 'GlonassCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GlonassCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
