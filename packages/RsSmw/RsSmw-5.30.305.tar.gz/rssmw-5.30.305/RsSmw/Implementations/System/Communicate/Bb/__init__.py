from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbCls:
	"""Bb commands group definition. 26 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bb", core, parent)

	@property
	def network(self):
		"""network commands group. 3 Sub-classes, 5 commands."""
		if not hasattr(self, '_network'):
			from .Network import NetworkCls
			self._network = NetworkCls(self._core, self._cmd_group)
		return self._network

	@property
	def qsfp(self):
		"""qsfp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_qsfp'):
			from .Qsfp import QsfpCls
			self._qsfp = QsfpCls(self._core, self._cmd_group)
		return self._qsfp

	def clone(self) -> 'BbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
