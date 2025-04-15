from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fmt3Cls:
	"""Fmt3 commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fmt3", core, parent)

	@property
	def occLength(self):
		"""occLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_occLength'):
			from .OccLength import OccLengthCls
			self._occLength = OccLengthCls(self._core, self._cmd_group)
		return self._occLength

	def clone(self) -> 'Fmt3Cls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fmt3Cls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
