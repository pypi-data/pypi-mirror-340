from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SrsCls:
	"""Srs commands group definition. 8 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("srs", core, parent)

	@property
	def bsrs(self):
		"""bsrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsrs'):
			from .Bsrs import BsrsCls
			self._bsrs = BsrsCls(self._core, self._cmd_group)
		return self._bsrs

	@property
	def cycShift(self):
		"""cycShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cycShift'):
			from .CycShift import CycShiftCls
			self._cycShift = CycShiftCls(self._core, self._cmd_group)
		return self._cycShift

	@property
	def naPort(self):
		"""naPort commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_naPort'):
			from .NaPort import NaPortCls
			self._naPort = NaPortCls(self._core, self._cmd_group)
		return self._naPort

	@property
	def nrrc(self):
		"""nrrc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrrc'):
			from .Nrrc import NrrcCls
			self._nrrc = NrrcCls(self._core, self._cmd_group)
		return self._nrrc

	@property
	def sym(self):
		"""sym commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sym'):
			from .Sym import SymCls
			self._sym = SymCls(self._core, self._cmd_group)
		return self._sym

	@property
	def trComb(self):
		"""trComb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trComb'):
			from .TrComb import TrCombCls
			self._trComb = TrCombCls(self._core, self._cmd_group)
		return self._trComb

	@property
	def tsrs(self):
		"""tsrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsrs'):
			from .Tsrs import TsrsCls
			self._tsrs = TsrsCls(self._core, self._cmd_group)
		return self._tsrs

	def clone(self) -> 'SrsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SrsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
