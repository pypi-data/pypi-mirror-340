from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmsCls:
	"""Dms commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dms", core, parent)

	@property
	def pz(self):
		"""pz commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pz'):
			from .Pz import PzCls
			self._pz = PzCls(self._core, self._cmd_group)
		return self._pz

	@property
	def wgs(self):
		"""wgs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wgs'):
			from .Wgs import WgsCls
			self._wgs = WgsCls(self._core, self._cmd_group)
		return self._wgs

	def clone(self) -> 'DmsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DmsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
