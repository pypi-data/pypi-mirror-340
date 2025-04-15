from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SlotCls:
	"""Slot commands group definition. 1 total commands, 1 Subgroups, 0 group commands
	Repeated Capability: SlotNull, default value after init: SlotNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("slot", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_slotNull_get', 'repcap_slotNull_set', repcap.SlotNull.Nr0)

	def repcap_slotNull_set(self, slotNull: repcap.SlotNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SlotNull.Default.
		Default value after init: SlotNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(slotNull)

	def repcap_slotNull_get(self) -> repcap.SlotNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def alloc(self):
		"""alloc commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_alloc'):
			from .Alloc import AllocCls
			self._alloc = AllocCls(self._core, self._cmd_group)
		return self._alloc

	def clone(self) -> 'SlotCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SlotCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
