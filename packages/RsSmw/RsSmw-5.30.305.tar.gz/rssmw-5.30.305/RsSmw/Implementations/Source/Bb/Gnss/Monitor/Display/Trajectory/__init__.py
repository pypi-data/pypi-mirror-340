from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TrajectoryCls:
	"""Trajectory commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trajectory", core, parent)

	@property
	def svid(self):
		"""svid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_svid'):
			from .Svid import SvidCls
			self._svid = SvidCls(self._core, self._cmd_group)
		return self._svid

	@property
	def system(self):
		"""system commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_system'):
			from .System import SystemCls
			self._system = SystemCls(self._core, self._cmd_group)
		return self._system

	def clone(self) -> 'TrajectoryCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TrajectoryCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
