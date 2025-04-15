from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RplCls:
	"""Rpl commands group definition. 9 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rpl", core, parent)

	@property
	def display(self):
		"""display commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_display'):
			from .Display import DisplayCls
			self._display = DisplayCls(self._core, self._cmd_group)
		return self._display

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .File import FileCls
			self._file = FileCls(self._core, self._cmd_group)
		return self._file

	@property
	def ilength(self):
		"""ilength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ilength'):
			from .Ilength import IlengthCls
			self._ilength = IlengthCls(self._core, self._cmd_group)
		return self._ilength

	@property
	def pmodel(self):
		"""pmodel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmodel'):
			from .Pmodel import PmodelCls
			self._pmodel = PmodelCls(self._core, self._cmd_group)
		return self._pmodel

	@property
	def predefined(self):
		"""predefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Predefined import PredefinedCls
			self._predefined = PredefinedCls(self._core, self._cmd_group)
		return self._predefined

	@property
	def roffset(self):
		"""roffset commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_roffset'):
			from .Roffset import RoffsetCls
			self._roffset = RoffsetCls(self._core, self._cmd_group)
		return self._roffset

	@property
	def rwindow(self):
		"""rwindow commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_rwindow'):
			from .Rwindow import RwindowCls
			self._rwindow = RwindowCls(self._core, self._cmd_group)
		return self._rwindow

	def clone(self) -> 'RplCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RplCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
