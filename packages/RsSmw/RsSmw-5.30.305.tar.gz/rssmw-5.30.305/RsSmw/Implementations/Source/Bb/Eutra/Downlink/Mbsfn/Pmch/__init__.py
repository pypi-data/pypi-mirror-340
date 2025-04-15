from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PmchCls:
	"""Pmch commands group definition. 10 total commands, 10 Subgroups, 0 group commands
	Repeated Capability: IndexNull, default value after init: IndexNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pmch", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_indexNull_get', 'repcap_indexNull_set', repcap.IndexNull.Nr0)

	def repcap_indexNull_set(self, indexNull: repcap.IndexNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IndexNull.Default.
		Default value after init: IndexNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(indexNull)

	def repcap_indexNull_get(self) -> repcap.IndexNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

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
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Mcs import McsCls
			self._mcs = McsCls(self._core, self._cmd_group)
		return self._mcs

	@property
	def mcsTwo(self):
		"""mcsTwo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcsTwo'):
			from .McsTwo import McsTwoCls
			self._mcsTwo = McsTwoCls(self._core, self._cmd_group)
		return self._mcsTwo

	@property
	def mod(self):
		"""mod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mod'):
			from .Mod import ModCls
			self._mod = ModCls(self._core, self._cmd_group)
		return self._mod

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def saEnd(self):
		"""saEnd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_saEnd'):
			from .SaEnd import SaEndCls
			self._saEnd = SaEndCls(self._core, self._cmd_group)
		return self._saEnd

	@property
	def saStart(self):
		"""saStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_saStart'):
			from .SaStart import SaStartCls
			self._saStart = SaStartCls(self._core, self._cmd_group)
		return self._saStart

	@property
	def speriod(self):
		"""speriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_speriod'):
			from .Speriod import SperiodCls
			self._speriod = SperiodCls(self._core, self._cmd_group)
		return self._speriod

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'PmchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PmchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
