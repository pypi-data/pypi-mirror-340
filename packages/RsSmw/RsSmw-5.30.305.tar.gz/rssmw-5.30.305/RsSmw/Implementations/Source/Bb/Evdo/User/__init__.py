from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 22 total commands, 11 Subgroups, 0 group commands
	Repeated Capability: UserIx, default value after init: UserIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_userIx_get', 'repcap_userIx_set', repcap.UserIx.Nr1)

	def repcap_userIx_set(self, userIx: repcap.UserIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to UserIx.Default.
		Default value after init: UserIx.Nr1"""
		self._cmd_group.set_repcap_enum_value(userIx)

	def repcap_userIx_get(self) -> repcap.UserIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def data(self):
		"""data commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def drclock(self):
		"""drclock commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_drclock'):
			from .Drclock import DrclockCls
			self._drclock = DrclockCls(self._core, self._cmd_group)
		return self._drclock

	@property
	def harq(self):
		"""harq commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Harq import HarqCls
			self._harq = HarqCls(self._core, self._cmd_group)
		return self._harq

	@property
	def ifactor(self):
		"""ifactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ifactor'):
			from .Ifactor import IfactorCls
			self._ifactor = IfactorCls(self._core, self._cmd_group)
		return self._ifactor

	@property
	def mac(self):
		"""mac commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_mac'):
			from .Mac import MacCls
			self._mac = MacCls(self._core, self._cmd_group)
		return self._mac

	@property
	def packet(self):
		"""packet commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_packet'):
			from .Packet import PacketCls
			self._packet = PacketCls(self._core, self._cmd_group)
		return self._packet

	@property
	def psize(self):
		"""psize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psize'):
			from .Psize import PsizeCls
			self._psize = PsizeCls(self._core, self._cmd_group)
		return self._psize

	@property
	def rate(self):
		"""rate commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_rate'):
			from .Rate import RateCls
			self._rate = RateCls(self._core, self._cmd_group)
		return self._rate

	@property
	def rpc(self):
		"""rpc commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_rpc'):
			from .Rpc import RpcCls
			self._rpc = RpcCls(self._core, self._cmd_group)
		return self._rpc

	@property
	def scount(self):
		"""scount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scount'):
			from .Scount import ScountCls
			self._scount = ScountCls(self._core, self._cmd_group)
		return self._scount

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'UserCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UserCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
