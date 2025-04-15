from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FnavCls:
	"""Fnav commands group definition. 44 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fnav", core, parent)

	@property
	def ccorrection(self):
		"""ccorrection commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccorrection'):
			from .Ccorrection import CcorrectionCls
			self._ccorrection = CcorrectionCls(self._core, self._cmd_group)
		return self._ccorrection

	@property
	def e5Advs(self):
		"""e5Advs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e5Advs'):
			from .E5Advs import E5AdvsCls
			self._e5Advs = E5AdvsCls(self._core, self._cmd_group)
		return self._e5Advs

	@property
	def e5Ahs(self):
		"""e5Ahs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e5Ahs'):
			from .E5Ahs import E5AhsCls
			self._e5Ahs = E5AhsCls(self._core, self._cmd_group)
		return self._e5Ahs

	@property
	def ephemeris(self):
		"""ephemeris commands group. 18 Sub-classes, 0 commands."""
		if not hasattr(self, '_ephemeris'):
			from .Ephemeris import EphemerisCls
			self._ephemeris = EphemerisCls(self._core, self._cmd_group)
		return self._ephemeris

	def clone(self) -> 'FnavCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FnavCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
