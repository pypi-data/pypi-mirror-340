from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UpCls:
	"""Up commands group definition. 150 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("up", core, parent)

	@property
	def cell(self):
		"""cell commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Cell import CellCls
			self._cell = CellCls(self._core, self._cmd_group)
		return self._cell

	@property
	def pparameter(self):
		"""pparameter commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pparameter'):
			from .Pparameter import PparameterCls
			self._pparameter = PparameterCls(self._core, self._cmd_group)
		return self._pparameter

	def clone(self) -> 'UpCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UpCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
