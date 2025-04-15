from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class M11TCls:
	"""M11T commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("m11T", core, parent)

	@property
	def foffset(self):
		"""foffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_foffset'):
			from .Foffset import FoffsetCls
			self._foffset = FoffsetCls(self._core, self._cmd_group)
		return self._foffset

	@property
	def lpair(self):
		"""lpair commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lpair'):
			from .Lpair import LpairCls
			self._lpair = LpairCls(self._core, self._cmd_group)
		return self._lpair

	@property
	def mbytes(self):
		"""mbytes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mbytes'):
			from .Mbytes import MbytesCls
			self._mbytes = MbytesCls(self._core, self._cmd_group)
		return self._mbytes

	@property
	def rframe(self):
		"""rframe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rframe'):
			from .Rframe import RframeCls
			self._rframe = RframeCls(self._core, self._cmd_group)
		return self._rframe

	@property
	def slot(self):
		"""slot commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_slot'):
			from .Slot import SlotCls
			self._slot = SlotCls(self._core, self._cmd_group)
		return self._slot

	def clone(self) -> 'M11TCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = M11TCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
