from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmrsCls:
	"""Dmrs commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmrs", core, parent)

	@property
	def scram(self):
		"""scram commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_scram'):
			from .Scram import ScramCls
			self._scram = ScramCls(self._core, self._cmd_group)
		return self._scram

	@property
	def space(self):
		"""space commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_space'):
			from .Space import SpaceCls
			self._space = SpaceCls(self._core, self._cmd_group)
		return self._space

	def clone(self) -> 'DmrsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DmrsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
