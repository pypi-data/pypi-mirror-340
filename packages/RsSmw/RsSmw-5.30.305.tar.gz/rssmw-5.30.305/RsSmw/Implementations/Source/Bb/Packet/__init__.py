from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PacketCls:
	"""Packet commands group definition. 3 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("packet", core, parent)

	@property
	def multiplex(self):
		"""multiplex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_multiplex'):
			from .Multiplex import MultiplexCls
			self._multiplex = MultiplexCls(self._core, self._cmd_group)
		return self._multiplex

	@property
	def unfiltered(self):
		"""unfiltered commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_unfiltered'):
			from .Unfiltered import UnfilteredCls
			self._unfiltered = UnfilteredCls(self._core, self._cmd_group)
		return self._unfiltered

	def clone(self) -> 'PacketCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PacketCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
