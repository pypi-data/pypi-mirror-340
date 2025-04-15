from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L5BandCls:
	"""L5Band commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("l5Band", core, parent)

	@property
	def l5S(self):
		"""l5S commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_l5S'):
			from .L5S import L5SCls
			self._l5S = L5SCls(self._core, self._cmd_group)
		return self._l5S

	def clone(self) -> 'L5BandCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L5BandCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
