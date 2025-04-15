from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McsCls:
	"""Mcs commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mcs", core, parent)

	@property
	def dpt(self):
		"""dpt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpt'):
			from .Dpt import DptCls
			self._dpt = DptCls(self._core, self._cmd_group)
		return self._dpt

	@property
	def fpt(self):
		"""fpt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fpt'):
			from .Fpt import FptCls
			self._fpt = FptCls(self._core, self._cmd_group)
		return self._fpt

	def clone(self) -> 'McsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = McsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
