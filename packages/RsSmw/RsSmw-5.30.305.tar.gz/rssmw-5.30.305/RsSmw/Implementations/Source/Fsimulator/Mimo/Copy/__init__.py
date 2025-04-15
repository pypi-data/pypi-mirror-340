from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CopyCls:
	"""Copy commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("copy", core, parent)

	@property
	def next(self):
		"""next commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_next'):
			from .Next import NextCls
			self._next = NextCls(self._core, self._cmd_group)
		return self._next

	@property
	def previous(self):
		"""previous commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_previous'):
			from .Previous import PreviousCls
			self._previous = PreviousCls(self._core, self._cmd_group)
		return self._previous

	def clone(self) -> 'CopyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CopyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
