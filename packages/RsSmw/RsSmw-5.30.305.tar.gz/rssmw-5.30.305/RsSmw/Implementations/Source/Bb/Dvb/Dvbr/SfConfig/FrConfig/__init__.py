from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrConfigCls:
	"""FrConfig commands group definition. 44 total commands, 12 Subgroups, 0 group commands
	Repeated Capability: FrCfgIxNull, default value after init: FrCfgIxNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frConfig", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_frCfgIxNull_get', 'repcap_frCfgIxNull_set', repcap.FrCfgIxNull.Nr0)

	def repcap_frCfgIxNull_set(self, frCfgIxNull: repcap.FrCfgIxNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to FrCfgIxNull.Default.
		Default value after init: FrCfgIxNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(frCfgIxNull)

	def repcap_frCfgIxNull_get(self) -> repcap.FrCfgIxNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def btu(self):
		"""btu commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_btu'):
			from .Btu import BtuCls
			self._btu = BtuCls(self._core, self._cmd_group)
		return self._btu

	@property
	def conflicts(self):
		"""conflicts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflicts'):
			from .Conflicts import ConflictsCls
			self._conflicts = ConflictsCls(self._core, self._cmd_group)
		return self._conflicts

	@property
	def frbw(self):
		"""frbw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frbw'):
			from .Frbw import FrbwCls
			self._frbw = FrbwCls(self._core, self._cmd_group)
		return self._frbw

	@property
	def frsTime(self):
		"""frsTime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frsTime'):
			from .FrsTime import FrsTimeCls
			self._frsTime = FrsTimeCls(self._core, self._cmd_group)
		return self._frsTime

	@property
	def grid(self):
		"""grid commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_grid'):
			from .Grid import GridCls
			self._grid = GridCls(self._core, self._cmd_group)
		return self._grid

	@property
	def grids(self):
		"""grids commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_grids'):
			from .Grids import GridsCls
			self._grids = GridsCls(self._core, self._cmd_group)
		return self._grids

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	@property
	def resolve(self):
		"""resolve commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_resolve'):
			from .Resolve import ResolveCls
			self._resolve = ResolveCls(self._core, self._cmd_group)
		return self._resolve

	@property
	def sec(self):
		"""sec commands group. 29 Sub-classes, 0 commands."""
		if not hasattr(self, '_sec'):
			from .Sec import SecCls
			self._sec = SecCls(self._core, self._cmd_group)
		return self._sec

	@property
	def sections(self):
		"""sections commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sections'):
			from .Sections import SectionsCls
			self._sections = SectionsCls(self._core, self._cmd_group)
		return self._sections

	@property
	def secIdx(self):
		"""secIdx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_secIdx'):
			from .SecIdx import SecIdxCls
			self._secIdx = SecIdxCls(self._core, self._cmd_group)
		return self._secIdx

	@property
	def txFormat(self):
		"""txFormat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txFormat'):
			from .TxFormat import TxFormatCls
			self._txFormat = TxFormatCls(self._core, self._cmd_group)
		return self._txFormat

	def clone(self) -> 'FrConfigCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrConfigCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
