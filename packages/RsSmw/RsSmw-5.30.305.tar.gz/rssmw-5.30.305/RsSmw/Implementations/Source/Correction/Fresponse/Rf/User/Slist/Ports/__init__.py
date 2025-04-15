from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PortsCls:
	"""Ports commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ports", core, parent)

	@property
	def fromPy(self):
		"""fromPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fromPy'):
			from .FromPy import FromPyCls
			self._fromPy = FromPyCls(self._core, self._cmd_group)
		return self._fromPy

	@property
	def to(self):
		"""to commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_to'):
			from .To import ToCls
			self._to = ToCls(self._core, self._cmd_group)
		return self._to

	def clone(self) -> 'PortsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PortsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
