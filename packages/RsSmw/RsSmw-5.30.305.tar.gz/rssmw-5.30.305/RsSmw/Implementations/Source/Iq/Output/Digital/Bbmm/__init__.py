from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbmmCls:
	"""Bbmm commands group definition. 25 total commands, 10 Subgroups, 0 group commands
	Repeated Capability: IqConnector, default value after init: IqConnector.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bbmm", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_iqConnector_get', 'repcap_iqConnector_set', repcap.IqConnector.Nr1)

	def repcap_iqConnector_set(self, iqConnector: repcap.IqConnector) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IqConnector.Default.
		Default value after init: IqConnector.Nr1"""
		self._cmd_group.set_repcap_enum_value(iqConnector)

	def repcap_iqConnector_get(self) -> repcap.IqConnector:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def cdevice(self):
		"""cdevice commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cdevice'):
			from .Cdevice import CdeviceCls
			self._cdevice = CdeviceCls(self._core, self._cmd_group)
		return self._cdevice

	@property
	def channel(self):
		"""channel commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	@property
	def gdelay(self):
		"""gdelay commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gdelay'):
			from .Gdelay import GdelayCls
			self._gdelay = GdelayCls(self._core, self._cmd_group)
		return self._gdelay

	@property
	def interface(self):
		"""interface commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interface'):
			from .Interface import InterfaceCls
			self._interface = InterfaceCls(self._core, self._cmd_group)
		return self._interface

	@property
	def oflow(self):
		"""oflow commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_oflow'):
			from .Oflow import OflowCls
			self._oflow = OflowCls(self._core, self._cmd_group)
		return self._oflow

	@property
	def pon(self):
		"""pon commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pon'):
			from .Pon import PonCls
			self._pon = PonCls(self._core, self._cmd_group)
		return self._pon

	@property
	def power(self):
		"""power commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def slow(self):
		"""slow commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_slow'):
			from .Slow import SlowCls
			self._slow = SlowCls(self._core, self._cmd_group)
		return self._slow

	@property
	def symbolRate(self):
		"""symbolRate commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'BbmmCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BbmmCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
