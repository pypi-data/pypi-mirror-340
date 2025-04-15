from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LfLocationCls:
	"""LfLocation commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lfLocation", core, parent)

	@property
	def coordinates(self):
		"""coordinates commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_coordinates'):
			from .Coordinates import CoordinatesCls
			self._coordinates = CoordinatesCls(self._core, self._cmd_group)
		return self._coordinates

	@property
	def height(self):
		"""height commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_height'):
			from .Height import HeightCls
			self._height = HeightCls(self._core, self._cmd_group)
		return self._height

	def clone(self) -> 'LfLocationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LfLocationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
