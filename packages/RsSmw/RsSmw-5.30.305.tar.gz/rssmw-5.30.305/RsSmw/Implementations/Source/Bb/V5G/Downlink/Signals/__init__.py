from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SignalsCls:
	"""Signals commands group definition. 2 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("signals", core, parent)

	@property
	def brs(self):
		"""brs commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_brs'):
			from .Brs import BrsCls
			self._brs = BrsCls(self._core, self._cmd_group)
		return self._brs

	def clone(self) -> 'SignalsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SignalsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
