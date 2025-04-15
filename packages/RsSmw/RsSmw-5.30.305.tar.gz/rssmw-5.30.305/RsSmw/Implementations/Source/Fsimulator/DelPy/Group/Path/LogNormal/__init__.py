from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LogNormalCls:
	"""LogNormal commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("logNormal", core, parent)

	@property
	def cstd(self):
		"""cstd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cstd'):
			from .Cstd import CstdCls
			self._cstd = CstdCls(self._core, self._cmd_group)
		return self._cstd

	@property
	def lconstant(self):
		"""lconstant commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lconstant'):
			from .Lconstant import LconstantCls
			self._lconstant = LconstantCls(self._core, self._cmd_group)
		return self._lconstant

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'LogNormalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LogNormalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
