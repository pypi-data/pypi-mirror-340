from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqCls:
	"""Iq commands group definition. 23 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iq", core, parent)

	@property
	def optimization(self):
		"""optimization commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_optimization'):
			from .Optimization import OptimizationCls
			self._optimization = OptimizationCls(self._core, self._cmd_group)
		return self._optimization

	@property
	def user(self):
		"""user commands group. 4 Sub-classes, 4 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	def clone(self) -> 'IqCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
