from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L5BandCls:
	"""L5Band commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("l5Band", core, parent)

	@property
	def e5A(self):
		"""e5A commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e5A'):
			from .E5A import E5ACls
			self._e5A = E5ACls(self._core, self._cmd_group)
		return self._e5A

	@property
	def e5B(self):
		"""e5B commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e5B'):
			from .E5B import E5BCls
			self._e5B = E5BCls(self._core, self._cmd_group)
		return self._e5B

	def clone(self) -> 'L5BandCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L5BandCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
