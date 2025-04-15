from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Del30Cls:
	"""Del30 commands group definition. 11 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("del30", core, parent)

	@property
	def group(self):
		"""group commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_group'):
			from .Group import GroupCls
			self._group = GroupCls(self._core, self._cmd_group)
		return self._group

	def clone(self) -> 'Del30Cls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Del30Cls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
