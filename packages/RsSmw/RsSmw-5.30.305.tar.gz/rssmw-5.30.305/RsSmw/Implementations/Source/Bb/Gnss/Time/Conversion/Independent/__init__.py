from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IndependentCls:
	"""Independent commands group definition. 5 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("independent", core, parent)

	@property
	def leap(self):
		"""leap commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_leap'):
			from .Leap import LeapCls
			self._leap = LeapCls(self._core, self._cmd_group)
		return self._leap

	def clone(self) -> 'IndependentCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IndependentCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
