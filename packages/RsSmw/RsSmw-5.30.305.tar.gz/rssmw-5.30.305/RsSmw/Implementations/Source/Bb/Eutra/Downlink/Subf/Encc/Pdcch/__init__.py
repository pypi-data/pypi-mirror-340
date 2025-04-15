from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PdcchCls:
	"""Pdcch commands group definition. 83 total commands, 14 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pdcch", core, parent)

	@property
	def alRegs(self):
		"""alRegs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alRegs'):
			from .AlRegs import AlRegsCls
			self._alRegs = AlRegsCls(self._core, self._cmd_group)
		return self._alRegs

	@property
	def avcces(self):
		"""avcces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_avcces'):
			from .Avcces import AvccesCls
			self._avcces = AvccesCls(self._core, self._cmd_group)
		return self._avcces

	@property
	def avRegs(self):
		"""avRegs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_avRegs'):
			from .AvRegs import AvRegsCls
			self._avRegs = AvRegsCls(self._core, self._cmd_group)
		return self._avRegs

	@property
	def bits(self):
		"""bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bits'):
			from .Bits import BitsCls
			self._bits = BitsCls(self._core, self._cmd_group)
		return self._bits

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dcRegs(self):
		"""dcRegs commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_dcRegs'):
			from .DcRegs import DcRegsCls
			self._dcRegs = DcRegsCls(self._core, self._cmd_group)
		return self._dcRegs

	@property
	def dregs(self):
		"""dregs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dregs'):
			from .Dregs import DregsCls
			self._dregs = DregsCls(self._core, self._cmd_group)
		return self._dregs

	@property
	def dselect(self):
		"""dselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselect'):
			from .Dselect import DselectCls
			self._dselect = DselectCls(self._core, self._cmd_group)
		return self._dselect

	@property
	def extc(self):
		"""extc commands group. 9 Sub-classes, 2 commands."""
		if not hasattr(self, '_extc'):
			from .Extc import ExtcCls
			self._extc = ExtcCls(self._core, self._cmd_group)
		return self._extc

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def noPdcchs(self):
		"""noPdcchs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noPdcchs'):
			from .NoPdcchs import NoPdcchsCls
			self._noPdcchs = NoPdcchsCls(self._core, self._cmd_group)
		return self._noPdcchs

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def scrambling(self):
		"""scrambling commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .Scrambling import ScramblingCls
			self._scrambling = ScramblingCls(self._core, self._cmd_group)
		return self._scrambling

	def clone(self) -> 'PdcchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PdcchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
