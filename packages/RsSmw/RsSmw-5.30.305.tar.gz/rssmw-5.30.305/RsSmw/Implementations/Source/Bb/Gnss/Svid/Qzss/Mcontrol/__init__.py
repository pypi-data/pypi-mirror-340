from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McontrolCls:
	"""Mcontrol commands group definition. 2 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mcontrol", core, parent)

	@property
	def copy(self):
		"""copy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_copy'):
			from .Copy import CopyCls
			self._copy = CopyCls(self._core, self._cmd_group)
		return self._copy

	def clone(self) -> 'McontrolCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = McontrolCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
