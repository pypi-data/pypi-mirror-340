from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WiringCls:
	"""Wiring commands group definition. 3 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("wiring", core, parent)

	@property
	def lo(self):
		"""lo commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_lo'):
			from .Lo import LoCls
			self._lo = LoCls(self._core, self._cmd_group)
		return self._lo

	@property
	def ref(self):
		"""ref commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ref'):
			from .Ref import RefCls
			self._ref = RefCls(self._core, self._cmd_group)
		return self._ref

	def clone(self) -> 'WiringCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = WiringCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
