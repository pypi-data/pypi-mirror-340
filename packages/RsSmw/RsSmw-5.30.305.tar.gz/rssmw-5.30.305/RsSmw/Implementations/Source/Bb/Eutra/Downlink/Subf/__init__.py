from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubfCls:
	"""Subf commands group definition. 131 total commands, 5 Subgroups, 0 group commands
	Repeated Capability: SubframeNull, default value after init: SubframeNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("subf", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_subframeNull_get', 'repcap_subframeNull_set', repcap.SubframeNull.Nr0)

	def repcap_subframeNull_set(self, subframeNull: repcap.SubframeNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SubframeNull.Default.
		Default value after init: SubframeNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(subframeNull)

	def repcap_subframeNull_get(self) -> repcap.SubframeNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def alCount(self):
		"""alCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alCount'):
			from .AlCount import AlCountCls
			self._alCount = AlCountCls(self._core, self._cmd_group)
		return self._alCount

	@property
	def alloc(self):
		"""alloc commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_alloc'):
			from .Alloc import AllocCls
			self._alloc = AllocCls(self._core, self._cmd_group)
		return self._alloc

	@property
	def cycPrefix(self):
		"""cycPrefix commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cycPrefix'):
			from .CycPrefix import CycPrefixCls
			self._cycPrefix = CycPrefixCls(self._core, self._cmd_group)
		return self._cycPrefix

	@property
	def encc(self):
		"""encc commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_encc'):
			from .Encc import EnccCls
			self._encc = EnccCls(self._core, self._cmd_group)
		return self._encc

	@property
	def user(self):
		"""user commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	def clone(self) -> 'SubfCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SubfCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
