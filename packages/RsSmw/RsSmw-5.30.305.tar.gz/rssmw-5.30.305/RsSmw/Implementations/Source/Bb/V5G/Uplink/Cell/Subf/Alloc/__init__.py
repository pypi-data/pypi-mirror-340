from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AllocCls:
	"""Alloc commands group definition. 38 total commands, 4 Subgroups, 0 group commands
	Repeated Capability: AllocationNull, default value after init: AllocationNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("alloc", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_allocationNull_get', 'repcap_allocationNull_set', repcap.AllocationNull.Nr0)

	def repcap_allocationNull_set(self, allocationNull: repcap.AllocationNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AllocationNull.Default.
		Default value after init: AllocationNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(allocationNull)

	def repcap_allocationNull_get(self) -> repcap.AllocationNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def pusch(self):
		"""pusch commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Pusch import PuschCls
			self._pusch = PuschCls(self._core, self._cmd_group)
		return self._pusch

	@property
	def xpucch(self):
		"""xpucch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_xpucch'):
			from .Xpucch import XpucchCls
			self._xpucch = XpucchCls(self._core, self._cmd_group)
		return self._xpucch

	@property
	def xpusch(self):
		"""xpusch commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_xpusch'):
			from .Xpusch import XpuschCls
			self._xpusch = XpuschCls(self._core, self._cmd_group)
		return self._xpusch

	@property
	def cw(self):
		"""cw commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cw'):
			from .Cw import CwCls
			self._cw = CwCls(self._core, self._cmd_group)
		return self._cw

	def clone(self) -> 'AllocCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AllocCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
