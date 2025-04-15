from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L1BandCls:
	"""L1Band commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("l1Band", core, parent)

	@property
	def e1Os(self):
		"""e1Os commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e1Os'):
			from .E1Os import E1OsCls
			self._e1Os = E1OsCls(self._core, self._cmd_group)
		return self._e1Os

	@property
	def e1Prs(self):
		"""e1Prs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e1Prs'):
			from .E1Prs import E1PrsCls
			self._e1Prs = E1PrsCls(self._core, self._cmd_group)
		return self._e1Prs

	def clone(self) -> 'L1BandCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L1BandCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
