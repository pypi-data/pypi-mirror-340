from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxCls:
	"""Rx commands group definition. 17 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rx", core, parent)

	@property
	def trajectory(self):
		"""trajectory commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_trajectory'):
			from .Trajectory import TrajectoryCls
			self._trajectory = TrajectoryCls(self._core, self._cmd_group)
		return self._trajectory

	@property
	def vehicle(self):
		"""vehicle commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_vehicle'):
			from .Vehicle import VehicleCls
			self._vehicle = VehicleCls(self._core, self._cmd_group)
		return self._vehicle

	def clone(self) -> 'RxCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
