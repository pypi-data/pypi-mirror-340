from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwpCls:
	"""Bwp commands group definition. 26 total commands, 7 Subgroups, 0 group commands
	Repeated Capability: BwPartNull, default value after init: BwPartNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bwp", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_bwPartNull_get', 'repcap_bwPartNull_set', repcap.BwPartNull.Nr0)

	def repcap_bwPartNull_set(self, bwPartNull: repcap.BwPartNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to BwPartNull.Default.
		Default value after init: BwPartNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(bwPartNull)

	def repcap_bwPartNull_get(self) -> repcap.BwPartNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Dfreq import DfreqCls
			self._dfreq = DfreqCls(self._core, self._cmd_group)
		return self._dfreq

	@property
	def indicator(self):
		"""indicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_indicator'):
			from .Indicator import IndicatorCls
			self._indicator = IndicatorCls(self._core, self._cmd_group)
		return self._indicator

	@property
	def paOffset(self):
		"""paOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paOffset'):
			from .PaOffset import PaOffsetCls
			self._paOffset = PaOffsetCls(self._core, self._cmd_group)
		return self._paOffset

	@property
	def rbNumber(self):
		"""rbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbNumber'):
			from .RbNumber import RbNumberCls
			self._rbNumber = RbNumberCls(self._core, self._cmd_group)
		return self._rbNumber

	@property
	def rbOffset(self):
		"""rbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbOffset'):
			from .RbOffset import RbOffsetCls
			self._rbOffset = RbOffsetCls(self._core, self._cmd_group)
		return self._rbOffset

	@property
	def resPool(self):
		"""resPool commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_resPool'):
			from .ResPool import ResPoolCls
			self._resPool = ResPoolCls(self._core, self._cmd_group)
		return self._resPool

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .ScSpacing import ScSpacingCls
			self._scSpacing = ScSpacingCls(self._core, self._cmd_group)
		return self._scSpacing

	def clone(self) -> 'BwpCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BwpCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
