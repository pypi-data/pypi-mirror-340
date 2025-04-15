from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InverseCls:
	"""Inverse commands group definition. 3 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inverse", core, parent)

	@property
	def matrix(self):
		"""matrix commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_matrix'):
			from .Matrix import MatrixCls
			self._matrix = MatrixCls(self._core, self._cmd_group)
		return self._matrix

	def clone(self) -> 'InverseCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InverseCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
