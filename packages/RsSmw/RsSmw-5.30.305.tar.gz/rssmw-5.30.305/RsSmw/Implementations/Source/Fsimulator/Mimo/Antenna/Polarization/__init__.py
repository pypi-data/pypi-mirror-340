from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PolarizationCls:
	"""Polarization commands group definition. 2 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("polarization", core, parent)

	@property
	def pratio(self):
		"""pratio commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pratio'):
			from .Pratio import PratioCls
			self._pratio = PratioCls(self._core, self._cmd_group)
		return self._pratio

	def clone(self) -> 'PolarizationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PolarizationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
