from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DerrorCls:
	"""Derror commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("derror", core, parent)

	@property
	def bit(self):
		"""bit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bit'):
			from .Bit import BitCls
			self._bit = BitCls(self._core, self._cmd_group)
		return self._bit

	@property
	def block(self):
		"""block commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_block'):
			from .Block import BlockCls
			self._block = BlockCls(self._core, self._cmd_group)
		return self._block

	def clone(self) -> 'DerrorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DerrorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
