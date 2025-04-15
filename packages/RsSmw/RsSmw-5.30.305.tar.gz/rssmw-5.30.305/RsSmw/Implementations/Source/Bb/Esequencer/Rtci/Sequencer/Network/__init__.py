from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NetworkCls:
	"""Network commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("network", core, parent)

	@property
	def hostname(self):
		"""hostname commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hostname'):
			from .Hostname import HostnameCls
			self._hostname = HostnameCls(self._core, self._cmd_group)
		return self._hostname

	@property
	def ipAddress(self):
		"""ipAddress commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ipAddress'):
			from .IpAddress import IpAddressCls
			self._ipAddress = IpAddressCls(self._core, self._cmd_group)
		return self._ipAddress

	@property
	def socket(self):
		"""socket commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_socket'):
			from .Socket import SocketCls
			self._socket = SocketCls(self._core, self._cmd_group)
		return self._socket

	@property
	def status(self):
		"""status commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_status'):
			from .Status import StatusCls
			self._status = StatusCls(self._core, self._cmd_group)
		return self._status

	def clone(self) -> 'NetworkCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NetworkCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
