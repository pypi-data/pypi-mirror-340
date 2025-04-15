from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TslCls:
	"""Tsl commands group definition. 8 total commands, 8 Subgroups, 0 group commands
	Repeated Capability: ChannelNull, default value after init: ChannelNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tsl", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channelNull_get', 'repcap_channelNull_set', repcap.ChannelNull.Nr0)

	def repcap_channelNull_set(self, channelNull: repcap.ChannelNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ChannelNull.Default.
		Default value after init: ChannelNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(channelNull)

	def repcap_channelNull_get(self) -> repcap.ChannelNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def ctype(self):
		"""ctype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctype'):
			from .Ctype import CtypeCls
			self._ctype = CtypeCls(self._core, self._cmd_group)
		return self._ctype

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dlist(self):
		"""dlist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlist'):
			from .Dlist import DlistCls
			self._dlist = DlistCls(self._core, self._cmd_group)
		return self._dlist

	@property
	def mcod(self):
		"""mcod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcod'):
			from .Mcod import McodCls
			self._mcod = McodCls(self._core, self._cmd_group)
		return self._mcod

	@property
	def nsym(self):
		"""nsym commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsym'):
			from .Nsym import NsymCls
			self._nsym = NsymCls(self._core, self._cmd_group)
		return self._nsym

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def pilots(self):
		"""pilots commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pilots'):
			from .Pilots import PilotsCls
			self._pilots = PilotsCls(self._core, self._cmd_group)
		return self._pilots

	@property
	def tsn(self):
		"""tsn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsn'):
			from .Tsn import TsnCls
			self._tsn = TsnCls(self._core, self._cmd_group)
		return self._tsn

	def clone(self) -> 'TslCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TslCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
