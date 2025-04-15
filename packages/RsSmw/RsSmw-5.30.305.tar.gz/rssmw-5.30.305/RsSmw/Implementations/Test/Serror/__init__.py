from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SerrorCls:
	"""Serror commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("serror", core, parent)

	@property
	def set(self):
		"""set commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_set'):
			from .Set import SetCls
			self._set = SetCls(self._core, self._cmd_group)
		return self._set

	@property
	def unset(self):
		"""unset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unset'):
			from .Unset import UnsetCls
			self._unset = UnsetCls(self._core, self._cmd_group)
		return self._unset

	def clone(self) -> 'SerrorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SerrorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
