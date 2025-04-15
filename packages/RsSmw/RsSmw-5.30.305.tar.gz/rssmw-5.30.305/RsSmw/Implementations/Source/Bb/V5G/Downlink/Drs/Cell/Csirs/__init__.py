from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsirsCls:
	"""Csirs commands group definition. 8 total commands, 8 Subgroups, 0 group commands
	Repeated Capability: CsiRefSignal, default value after init: CsiRefSignal.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csirs", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_csiRefSignal_get', 'repcap_csiRefSignal_set', repcap.CsiRefSignal.Nr1)

	def repcap_csiRefSignal_set(self, csiRefSignal: repcap.CsiRefSignal) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CsiRefSignal.Default.
		Default value after init: CsiRefSignal.Nr1"""
		self._cmd_group.set_repcap_enum_value(csiRefSignal)

	def repcap_csiRefSignal_get(self) -> repcap.CsiRefSignal:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def nzConfig(self):
		"""nzConfig commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nzConfig'):
			from .NzConfig import NzConfigCls
			self._nzConfig = NzConfigCls(self._core, self._cmd_group)
		return self._nzConfig

	@property
	def nzqOffset(self):
		"""nzqOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nzqOffset'):
			from .NzqOffset import NzqOffsetCls
			self._nzqOffset = NzqOffsetCls(self._core, self._cmd_group)
		return self._nzqOffset

	@property
	def nzsCid(self):
		"""nzsCid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nzsCid'):
			from .NzsCid import NzsCidCls
			self._nzsCid = NzsCidCls(self._core, self._cmd_group)
		return self._nzsCid

	@property
	def nzsfOffset(self):
		"""nzsfOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nzsfOffset'):
			from .NzsfOffset import NzsfOffsetCls
			self._nzsfOffset = NzsfOffsetCls(self._core, self._cmd_group)
		return self._nzsfOffset

	@property
	def zp(self):
		"""zp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zp'):
			from .Zp import ZpCls
			self._zp = ZpCls(self._core, self._cmd_group)
		return self._zp

	@property
	def zpDelta(self):
		"""zpDelta commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zpDelta'):
			from .ZpDelta import ZpDeltaCls
			self._zpDelta = ZpDeltaCls(self._core, self._cmd_group)
		return self._zpDelta

	@property
	def zpi(self):
		"""zpi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zpi'):
			from .Zpi import ZpiCls
			self._zpi = ZpiCls(self._core, self._cmd_group)
		return self._zpi

	@property
	def zpt(self):
		"""zpt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zpt'):
			from .Zpt import ZptCls
			self._zpt = ZptCls(self._core, self._cmd_group)
		return self._zpt

	def clone(self) -> 'CsirsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsirsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
