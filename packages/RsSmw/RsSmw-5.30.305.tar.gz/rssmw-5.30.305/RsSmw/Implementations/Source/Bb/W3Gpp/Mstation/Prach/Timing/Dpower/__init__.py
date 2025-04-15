from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DpowerCls:
	"""Dpower commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dpower", core, parent)

	@property
	def mpart(self):
		"""mpart commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_mpart'):
			from .Mpart import MpartCls
			self._mpart = MpartCls(self._core, self._cmd_group)
		return self._mpart

	@property
	def preamble(self):
		"""preamble commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_preamble'):
			from .Preamble import PreambleCls
			self._preamble = PreambleCls(self._core, self._cmd_group)
		return self._preamble

	def clone(self) -> 'DpowerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DpowerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
