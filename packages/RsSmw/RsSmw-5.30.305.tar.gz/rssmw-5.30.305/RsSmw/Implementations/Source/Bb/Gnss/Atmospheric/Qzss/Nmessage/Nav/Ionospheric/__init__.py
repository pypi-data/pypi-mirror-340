from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IonosphericCls:
	"""Ionospheric commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ionospheric", core, parent)

	@property
	def alpha(self):
		"""alpha commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_alpha'):
			from .Alpha import AlphaCls
			self._alpha = AlphaCls(self._core, self._cmd_group)
		return self._alpha

	@property
	def beta(self):
		"""beta commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_beta'):
			from .Beta import BetaCls
			self._beta = BetaCls(self._core, self._cmd_group)
		return self._beta

	def clone(self) -> 'IonosphericCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IonosphericCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
