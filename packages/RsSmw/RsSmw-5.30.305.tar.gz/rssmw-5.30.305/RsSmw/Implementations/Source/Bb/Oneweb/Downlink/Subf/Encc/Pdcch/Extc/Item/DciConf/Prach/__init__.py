from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrachCls:
	"""Prach commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("prach", core, parent)

	@property
	def mindex(self):
		"""mindex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mindex'):
			from .Mindex import MindexCls
			self._mindex = MindexCls(self._core, self._cmd_group)
		return self._mindex

	@property
	def prIndex(self):
		"""prIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prIndex'):
			from .PrIndex import PrIndexCls
			self._prIndex = PrIndexCls(self._core, self._cmd_group)
		return self._prIndex

	def clone(self) -> 'PrachCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PrachCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
