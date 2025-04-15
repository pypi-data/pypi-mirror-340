from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L1BandCls:
	"""L1Band commands group definition. 9 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("l1Band", core, parent)

	@property
	def x1S(self):
		"""x1S commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_x1S'):
			from .X1S import X1SCls
			self._x1S = X1SCls(self._core, self._cmd_group)
		return self._x1S

	def clone(self) -> 'L1BandCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L1BandCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
