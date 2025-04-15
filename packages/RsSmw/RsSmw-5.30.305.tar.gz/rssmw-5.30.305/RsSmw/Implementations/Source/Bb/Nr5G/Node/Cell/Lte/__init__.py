from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LteCls:
	"""Lte commands group definition. 6 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lte", core, parent)

	@property
	def npat(self):
		"""npat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_npat'):
			from .Npat import NpatCls
			self._npat = NpatCls(self._core, self._cmd_group)
		return self._npat

	@property
	def patt(self):
		"""patt commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_patt'):
			from .Patt import PattCls
			self._patt = PattCls(self._core, self._cmd_group)
		return self._patt

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'LteCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LteCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
