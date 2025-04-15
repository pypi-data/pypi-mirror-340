from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NavCls:
	"""Nav commands group definition. 36 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nav", core, parent)

	@property
	def ccorrection(self):
		"""ccorrection commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccorrection'):
			from .Ccorrection import CcorrectionCls
			self._ccorrection = CcorrectionCls(self._core, self._cmd_group)
		return self._ccorrection

	@property
	def ephemeris(self):
		"""ephemeris commands group. 19 Sub-classes, 0 commands."""
		if not hasattr(self, '_ephemeris'):
			from .Ephemeris import EphemerisCls
			self._ephemeris = EphemerisCls(self._core, self._cmd_group)
		return self._ephemeris

	def clone(self) -> 'NavCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NavCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
