from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SetCls:
	"""Set commands group definition. 2 total commands, 2 Subgroups, 0 group commands
	Repeated Capability: SetItem, default value after init: SetItem.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("set", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_setItem_get', 'repcap_setItem_set', repcap.SetItem.Nr1)

	def repcap_setItem_set(self, setItem: repcap.SetItem) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SetItem.Default.
		Default value after init: SetItem.Nr1"""
		self._cmd_group.set_repcap_enum_value(setItem)

	def repcap_setItem_get(self) -> repcap.SetItem:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def rbCount(self):
		"""rbCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbCount'):
			from .RbCount import RbCountCls
			self._rbCount = RbCountCls(self._core, self._cmd_group)
		return self._rbCount

	@property
	def vrbOffset(self):
		"""vrbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vrbOffset'):
			from .VrbOffset import VrbOffsetCls
			self._vrbOffset = VrbOffsetCls(self._core, self._cmd_group)
		return self._vrbOffset

	def clone(self) -> 'SetCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SetCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
