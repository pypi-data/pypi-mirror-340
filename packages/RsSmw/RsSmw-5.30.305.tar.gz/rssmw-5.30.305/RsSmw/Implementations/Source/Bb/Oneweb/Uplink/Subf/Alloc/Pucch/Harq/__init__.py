from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HarqCls:
	"""Harq commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("harq", core, parent)

	@property
	def anPattern(self):
		"""anPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_anPattern'):
			from .AnPattern import AnPatternCls
			self._anPattern = AnPatternCls(self._core, self._cmd_group)
		return self._anPattern

	@property
	def bits(self):
		"""bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bits'):
			from .Bits import BitsCls
			self._bits = BitsCls(self._core, self._cmd_group)
		return self._bits

	@property
	def cbits(self):
		"""cbits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbits'):
			from .Cbits import CbitsCls
			self._cbits = CbitsCls(self._core, self._cmd_group)
		return self._cbits

	def clone(self) -> 'HarqCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HarqCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
