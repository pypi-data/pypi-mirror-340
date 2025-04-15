from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CellCls:
	"""Cell commands group definition. 28 total commands, 6 Subgroups, 0 group commands
	Repeated Capability: CellNull, default value after init: CellNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cell", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_cellNull_get', 'repcap_cellNull_set', repcap.CellNull.Nr0)

	def repcap_cellNull_set(self, cellNull: repcap.CellNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CellNull.Default.
		Default value after init: CellNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(cellNull)

	def repcap_cellNull_get(self) -> repcap.CellNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def row(self):
		"""row commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_row'):
			from .Row import RowCls
			self._row = RowCls(self._core, self._cmd_group)
		return self._row

	@property
	def eimta(self):
		"""eimta commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_eimta'):
			from .Eimta import EimtaCls
			self._eimta = EimtaCls(self._core, self._cmd_group)
		return self._eimta

	@property
	def frc(self):
		"""frc commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_frc'):
			from .Frc import FrcCls
			self._frc = FrcCls(self._core, self._cmd_group)
		return self._frc

	@property
	def pusch(self):
		"""pusch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Pusch import PuschCls
			self._pusch = PuschCls(self._core, self._cmd_group)
		return self._pusch

	@property
	def refsig(self):
		"""refsig commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_refsig'):
			from .Refsig import RefsigCls
			self._refsig = RefsigCls(self._core, self._cmd_group)
		return self._refsig

	@property
	def xpusch(self):
		"""xpusch commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_xpusch'):
			from .Xpusch import XpuschCls
			self._xpusch = XpuschCls(self._core, self._cmd_group)
		return self._xpusch

	def clone(self) -> 'CellCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CellCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
